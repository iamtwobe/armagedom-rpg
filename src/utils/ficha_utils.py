

def get_pericias(ficha):
    return [
        ("Acrobacia", ficha.p_acrobacia, "Des"),
        ("Adestramento", ficha.p_adestramento, "Int"),
        ("Artes", ficha.p_artes, "Car"),
        ("Atletismo", ficha.p_atletismo, "For"),
        ("Ciências", ficha.p_ciencias, "Int"),
        ("Crime", ficha.p_crime, "Des"),
        ("Enganação", ficha.p_enganacao, "Car"),
        ("Fortitude", ficha.p_fortitude, "Con"),
        ("Furtividade", ficha.p_furtividade, "Des"),
        ("Iniciativa", ficha.p_iniciativa, "Des"),
        ("Intimidação", ficha.p_intimidacao, "Car"),
        ("Intuição", ficha.p_intuicao, "Int"),
        ("Investigação", ficha.p_investigacao, "Int"),
        ("Luta", ficha.p_luta, "For"),
        ("Medicina", ficha.p_medicina, "Int"),
        (ficha.oficio_nome, ficha.p_oficio, ficha.oficio_atributo[:3].capitalize()),
        ("Percepção", ficha.p_percepcao, "Des"),
        ("Persuasão", ficha.p_persuasao, "Car"),
        ("Pilotagem", ficha.p_pilotagem, "Des"),
        ("Pontaria", ficha.p_pontaria, "Des"),
        ("Reflexos", ficha.p_reflexos, "Des"),
        ("Religião", ficha.p_religiao, "Int"),
        ("Sobrevivência", ficha.p_sobrevivencia, "Int"),
        ("Tática", ficha.p_tatica, "Des"),
        ("Tecnologia", ficha.p_tecnologia, "Int"),
        ("História", ficha.p_historia, "Int"),
        ("Vontade", ficha.p_vontade, "Car")
    ]

_pericias_format = {
    "ciências":"ciencias",
    "enganação":"enganacao",
    "intimidação":"intimidacao",
    "intuição":"intuicao",
    "investigação":"investigacao",
    "percepção":"percepcao",
    "persuasão":"persuasao",
    "religião":"religiao",
    "sobrevivência":"sobrevivencia",
    "tática":"tatica",
    "história":"historia"
}