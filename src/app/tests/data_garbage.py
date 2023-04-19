import datetime

RUSSIAN_CONS_DATA = {
    "Russia": {
        "LOC": {
            "рф": [
                "6fdc9ad0-5fc4-4037-b4a7-0d1fd1a5efef",
                "3c9c4d17-65ba-44be-9b33-4c24f3d20048",
            ],
            "сша": [
                "a13c9dc0-7628-4bf6-bf8c-fb968e440826",
                "2b7a8a3e-808d-4326-9215-aa7026edea19",
            ],
        },
        "ORG": {
            "цб": [
                "fff5b484-262e-4c9f-bf93-e957e898aded",
                "4805e20c-6908-43d5-ae6a-49bf219b0a1d",
            ],
            "всу": ["827b7625-1110-4e51-9c43-c26b09a23dbc"],
        },
        "PER": {
            "Херш": [
                "b61eb586-eed7-47e6-ac50-e8e1b1177e3b",
                "8aa5d169-4944-466d-ab51-f22f55bcf002",
            ],
            "Путин": ["b04f697c-a7a0-48c4-ab79-6a92a308758e"],
        },
    }
}
TEST_TITLES = [
    {
        "url": "https://www.kommersant.ru/",
        "href": "https://www.kommersant.ru/doc/5826303?from=main",
        "lang": "RU",
        "time": str(datetime.date.today()),
        "title": "Евросоюз перевел РФ из серого в черный список «налоговых убежищ",
        "country": "Russia",
    },
    {
        "url": "https://www.ktrtrtr.ru/",
        "href": "https://www.kommersant.rasdsadasdas",
        "lang": "RU",
        "time": str(datetime.date.today()),
        "title": "TEST tilzdfnsjk;fnk",
        "country": "Russia",
    },
    {
        "url": "https://www.cgnznzgn.ru/",
        "href": "https://www.kommersantafFGASwqrs",
        "lang": "RU",
        "time": str(datetime.date.today()),
        "title": "TEST ASFasasffas",
        "country": "Russia",
    },
]
