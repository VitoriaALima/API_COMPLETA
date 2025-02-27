from flask import Flask, jsonify, request
from main import app, con

@app.route('/livros',methods=['GET'])
def livro():
    cursor = con.cursor()
    cursor.execute("SELECT id_livro, titulo, autor, ano_publicacao FROM livros")
    livros = cursor.fetchall()
    livros_dic = []
    for livro in livros:
        livros_dic.append({
            'id_livro': livro[0],
            'titulo': livro[1],
            'autor': livro[2],
            'ano_publicacao': livro[3]
        })

    return jsonify(mensagem='Lista de livros', livros=livros_dic)

@app.route('/livros', methods=['POST'])
def livros_post():
    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    ano_publicacao = data.get('ano_publicacao')

    cursor = con.cursor()
    cursor.execute("SELECT 1 FROM LIVROS WHERE TITULO = ?" , (titulo,))

    if cursor.fetchone():
        return jsonify("Livro já cadastrado")

    cursor.execute("INSERT INTO LIVROS(TITULO, AUTOR, ANO_PUBLICACAO) VALUES (?,?,?)",
                   (titulo, autor, ano_publicacao))

    con.commit()
    cursor.close()

    return jsonify({
        'message': "Livro cadastrado com sucesso!",
        'livros': {
            'titulo': titulo,
            'autor': autor,
            'ano_publicacao': ano_publicacao
        }
    })

@app.route('/livros/<int:id>', methods=['PUT'])
def livros_put(id):
    cursor = con.cursor()
    cursor.execute("select id_livro, titulo, autor, ano_publicacao from livros where id_livro = ?", (id,))
    livro_data = cursor.fetchone()

    if not livro_data:
        cursor.close()
        return jsonify({"error": "Livro não encontrado"}), 404

    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    ano_publicacao = data.get('ano_publicacao')

    cursor.execute("UPDATE livros SET TITULO = ?, AUTOR = ?, ANO_Pu"
                   "BLICACAO = ? WHERE ID_LIVRO = ?",
                   (titulo, autor, ano_publicacao, id))

    con.commit()
    cursor.close()

    return jsonify({
        'message': "Livro atualizado com sucesso!",
        'livro': {
            'titulo': titulo,
            'autor': autor,
            'ano_publicacao': ano_publicacao
        }
    })