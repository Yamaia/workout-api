from tests.conftest import atleta_payload, preparar_base


async def test_criar_e_buscar_atleta(client):
    await preparar_base(client)
    r = await client.post("/atletas/", json=atleta_payload())
    assert r.status_code == 201
    corpo = r.json()
    assert corpo["categoria"] == {"nome": "Scale"}
    assert corpo["centro_treinamento"] == {"nome": "CT King"}
    r = await client.get(f"/atletas/{corpo['id']}")
    assert r.status_code == 200 and r.json()["cpf"] == "12345678900"


async def test_cpf_duplicado_retorna_303_com_mensagem(client):
    await preparar_base(client)
    await client.post("/atletas/", json=atleta_payload())
    r = await client.post("/atletas/", json=atleta_payload(nome="Maria"))
    assert r.status_code == 303
    assert r.json()["detail"] == "Já existe um atleta cadastrado com o cpf: 12345678900"


async def test_categoria_e_centro_duplicados_retornam_303(client):
    await preparar_base(client)
    r = await client.post("/categorias/", json={"nome": "Scale"})
    assert r.status_code == 303
    assert r.json()["detail"] == "Já existe uma categoria cadastrada com o nome: Scale"
    r = await client.post("/centros_treinamento/", json={"nome": "CT King", "endereco": "x", "proprietario": "y"})
    assert r.status_code == 303
    assert r.json()["detail"] == "Já existe um centro de treinamento cadastrado com o nome: CT King"


async def test_categoria_inexistente_retorna_400(client):
    await preparar_base(client)
    r = await client.post("/atletas/", json=atleta_payload(categoria={"nome": "RX"}))
    assert r.status_code == 400


async def test_get_all_customizado_e_paginado(client):
    await preparar_base(client)
    for i in range(5):
        await client.post("/atletas/", json=atleta_payload(nome=f"Atleta {i}", cpf=f"1234567890{i}"))
    r = await client.get("/atletas/")
    assert r.status_code == 200
    corpo = r.json()
    assert corpo["total"] == 5 and corpo["limit"] == 50 and corpo["offset"] == 0
    assert corpo["items"][0] == {"nome": "Atleta 0", "centro_treinamento": "CT King", "categoria": "Scale"}

    r = await client.get("/atletas/", params={"limit": 2, "offset": 2})
    corpo = r.json()
    assert [i["nome"] for i in corpo["items"]] == ["Atleta 2", "Atleta 3"]
    assert corpo["total"] == 5 and corpo["limit"] == 2 and corpo["offset"] == 2


async def test_query_params_nome_e_cpf(client):
    await preparar_base(client)
    await client.post("/atletas/", json=atleta_payload(nome="Joao Silva", cpf="11111111111"))
    await client.post("/atletas/", json=atleta_payload(nome="Maria Souza", cpf="22222222222"))
    por_nome = (await client.get("/atletas/", params={"nome": "silva"})).json()
    assert [i["nome"] for i in por_nome["items"]] == ["Joao Silva"]
    por_cpf = (await client.get("/atletas/", params={"cpf": "22222222222"})).json()
    assert [i["nome"] for i in por_cpf["items"]] == ["Maria Souza"]


async def test_editar_e_remover(client):
    await preparar_base(client)
    id_ = (await client.post("/atletas/", json=atleta_payload())).json()["id"]
    r = await client.patch(f"/atletas/{id_}", json={"nome": "Joao Pedro"})
    assert r.status_code == 200 and r.json()["nome"] == "Joao Pedro"
    assert (await client.delete(f"/atletas/{id_}")).status_code == 204
    assert (await client.get(f"/atletas/{id_}")).status_code == 404


async def test_validacao_de_cpf(client):
    await preparar_base(client)
    r = await client.post("/atletas/", json=atleta_payload(cpf="123"))
    assert r.status_code == 422
