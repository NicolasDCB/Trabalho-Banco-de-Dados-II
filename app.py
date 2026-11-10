import os
import sqlite3
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DB_PATH = os.path.join(app.root_path, 'prompts.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Tabela principal da atividade / prompt base
    conn.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT DEFAULT 'Nicolas / Nathan',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela de versoes para armazenar a evolucao do prompt (v1, v2, v3...)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS prompt_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_id INTEGER NOT NULL,
            version_number INTEGER NOT NULL DEFAULT 1,
            text TEXT NOT NULL,
            change_notes TEXT DEFAULT 'Versão inicial',
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (activity_id) REFERENCES activities (id) ON DELETE CASCADE
        )
    ''')

    # Insere um exemplo inicial caso o banco esteja vazio
    count = conn.execute('SELECT COUNT(*) FROM activities').fetchone()[0]
    if count == 0:
        cur = conn.execute(
            "INSERT INTO activities (title, author) VALUES (?, ?)",
            ("Gerador de Consultas SQL", "Nathan e Nicolas")
        )
        act_id = cur.lastrowid
        conn.execute(
            "INSERT INTO prompt_versions (activity_id, version_number, text, change_notes) VALUES (?, ?, ?, ?)",
            (act_id, 1, "Crie uma consulta SQL para buscar clientes.", "Versão inicial simples (v1)")
        )
        conn.execute(
            "INSERT INTO prompt_versions (activity_id, version_number, text, change_notes) VALUES (?, ?, ?, ?)",
            (act_id, 2, "Atue como especialista em banco de dados. Crie uma query SQL para a tabela clientes(id, nome, email) ordenando por nome.", "Adicionou contexto das colunas e ordenação (v2)")
        )
        conn.commit()

    return conn


def salvar_imagem(image_file):
    if image_file and image_file.filename:
        nome_seguro = secure_filename(image_file.filename)
        if nome_seguro:
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], nome_seguro)
            image_file.save(full_path)
            return f"uploads/{nome_seguro}"
    return ""


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db()

    # Cadastrar um novo prompt base (ja cria a versao v1)
    if request.method == 'POST':
        title = request.form.get('title', '').strip() or 'Atividade de Prompt'
        author = request.form.get('author', '').strip() or 'Nathan e Nicolas'
        prompt_text = request.form.get('prompt', '').strip()
        img_path = salvar_imagem(request.files.get('image'))

        if prompt_text:
            cur = conn.execute(
                'INSERT INTO activities (title, author) VALUES (?, ?)',
                (title, author)
            )
            activity_id = cur.lastrowid

            conn.execute(
                '''
                INSERT INTO prompt_versions (activity_id, version_number, text, change_notes, image_path)
                VALUES (?, 1, ?, ?, ?)
                ''',
                (activity_id, prompt_text, 'Versão inicial (v1)', img_path)
            )
            conn.commit()

        conn.close()
        return redirect(url_for('index'))

    # Buscar todas as atividades e suas versoes do banco
    activities_rows = conn.execute('SELECT * FROM activities ORDER BY id DESC').fetchall()
    activities = []

    for act in activities_rows:
        versions = conn.execute(
            'SELECT * FROM prompt_versions WHERE activity_id = ? ORDER BY version_number ASC',
            (act['id'],)
        ).fetchall()

        ultima_versao_texto = versions[-1]['text'] if versions else ''
        activities.append({
            'id': act['id'],
            'title': act['title'],
            'author': act['author'],
            'created_at': act['created_at'],
            'versions': versions,
            'latest_text': ultima_versao_texto,
            'next_version': len(versions) + 1
        })

    conn.close()
    return render_template('index.html', activities=activities)


@app.route('/evolve/<int:activity_id>', methods=['POST'])
def evolve_prompt(activity_id):
    """Recebe uma nova versao de um prompt existente no banco e salva na evolucao."""
    prompt_text = request.form.get('prompt', '').strip()
    change_notes = request.form.get('change_notes', '').strip() or 'Evolução do prompt'
    img_path = salvar_imagem(request.files.get('image'))

    if prompt_text:
        conn = get_db()
        row = conn.execute(
            'SELECT COALESCE(MAX(version_number), 0) + 1 AS prox FROM prompt_versions WHERE activity_id = ?',
            (activity_id,)
        ).fetchone()
        prox_versao = row['prox']

        conn.execute(
            '''
            INSERT INTO prompt_versions (activity_id, version_number, text, change_notes, image_path)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (activity_id, prox_versao, prompt_text, change_notes, img_path)
        )
        conn.commit()
        conn.close()

    return redirect(url_for('index'))


@app.route('/delete/<int:activity_id>', methods=['POST'])
def delete_activity(activity_id):
    conn = get_db()
    conn.execute('DELETE FROM prompt_versions WHERE activity_id = ?', (activity_id,))
    conn.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
