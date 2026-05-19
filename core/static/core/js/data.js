// Locais historicos da Mesorregiao Grande Fronteira do Mercosul
var LOCAIS = [
  {
    id: 1,
    nome: "Forte Marechal Luz",
    categoria: "forte",
    cidade: "São Francisco do Sul",
    uf: "SC",
    endereco: "Av. Atlântica, s/n — Praia do Forte",
    lat: -26.2089, lng: -48.5483,
    periodo: "1909",
    resumo: "Fortificação militar de defesa costeira erguida no início do século XX.",
    descricao: "Construído entre 1908 e 1909 sobre as ruínas de antigas baterias coloniais portuguesas, o Forte Marechal Luz integra o sistema defensivo da Baía da Babitonga. Sua artilharia, originalmente Krupp, foi pensada para proteger o canal de acesso ao porto de São Francisco do Sul. Hoje preserva quartéis, casamatas e uma capela tombada, e recebe visitação guiada que articula memória militar e história do litoral catarinense.",
    imagens: [["#1f3a5f","#0b2545"],["#2c4a6e","#143872"],["#3d5a7d","#1f4a8f"]]
  },
  {
    id: 2,
    nome: "Ruínas de São Miguel das Missões",
    categoria: "ruina",
    cidade: "São Miguel das Missões",
    uf: "RS",
    endereco: "Rua São Luiz Gonzaga, s/n — Centro",
    lat: -28.5550, lng: -54.5610,
    periodo: "1735–1745",
    resumo: "Patrimônio Mundial da UNESCO. Remanescente das reduções jesuítico-guaranis.",
    descricao: "Erguida pelo padre Gianbattista Primoli, a igreja de São Miguel Arcanjo é o testemunho mais imponente das missões jesuítico-guaranis no território brasileiro. Tombada pela UNESCO em 1983, suas ruínas em arenito vermelho preservam a fachada barroca e a planta retangular, ladeadas pelo Museu das Missões projetado por Lucio Costa em 1940. O sítio articula memórias do encontro entre povos guaranis e missionários jesuítas, e da subsequente dispersão guaranítica do século XVIII.",
    imagens: [["#7a3520","#3a1a0e"],["#9a5034","#5a2a18"],["#b06a4a","#7a3520"]]
  },
  {
    id: 3,
    nome: "Museu Histórico Antônio Selistre de Campos",
    categoria: "museu",
    cidade: "Chapecó",
    uf: "SC",
    endereco: "Av. Getúlio Vargas, 168N — Centro",
    lat: -27.0975, lng: -52.6190,
    periodo: "Acervo desde 1917",
    resumo: "Acervo sobre colonização do oeste catarinense e a Guerra do Contestado.",
    descricao: "Instalado num casarão histórico do centro de Chapecó, o museu reúne documentação sobre os ciclos de colonização do oeste catarinense, a presença indígena kaingang, a Guerra do Contestado (1912–1916) e a urbanização da região. Leva o nome do magistrado e historiador que primeiro sistematizou parte desse acervo. É hoje uma das principais referências para pesquisadores que trabalham a fronteira sul a partir das fontes locais.",
    imagens: [["#3a4a3c","#1a2a1e"],["#5a6a5c","#3a4a3c"],["#7a8a7c","#5a6a5c"]]
  },
  {
    id: 4,
    nome: "Marco das Três Fronteiras",
    categoria: "marco",
    cidade: "Foz do Iguaçu",
    uf: "PR",
    endereco: "Av. General Meira, s/n — Vila Portes",
    lat: -25.5950, lng: -54.5870,
    periodo: "1903",
    resumo: "Obelisco que marca o encontro de Brasil, Argentina e Paraguai.",
    descricao: "Erguido em 1903 às margens do encontro dos rios Iguaçu e Paraná, o marco brasileiro é gêmeo de outros dois — argentino e paraguaio — pintados nas cores das respectivas bandeiras. Para além do apelo turístico contemporâneo, o lugar concentra discussões sobre fronteira, soberania e os fluxos transnacionais que estruturam o cotidiano da tríplice fronteira: trabalho, comércio, migração e cooperação cultural.",
    imagens: [["#2d6a4f","#0f3825"],["#52b788","#2d6a4f"],["#74c69d","#52b788"]]
  },
  {
    id: 5,
    nome: "Igreja Matriz Santo Antônio",
    categoria: "igreja",
    cidade: "Erechim",
    uf: "RS",
    endereco: "Praça da Bandeira, s/n — Centro",
    lat: -27.6340, lng: -52.2740,
    periodo: "1957",
    resumo: "Catedral neogótica símbolo da colonização italiana no Alto Uruguai.",
    descricao: "Concluída em 1957 sobre as fundações de uma capela de 1922, a Catedral Santo Antônio é referência arquitetônica da imigração italiana no Alto Uruguai gaúcho. Suas torres de 56 metros, vitrais em mosaico e estrutura em concreto armado a tornam uma das maiores igrejas neogóticas do sul do país. O conjunto da praça concentra memória do processo de colonização dirigida que reconfigurou o noroeste do Rio Grande do Sul a partir do início do século XX.",
    imagens: [["#5a4a3a","#2a1a0e"],["#7a6a5a","#4a3a2a"],["#9a8a7a","#6a5a4a"]]
  },
  {
    id: 6,
    nome: "Cemitério dos Pelados — Trincheira do Irani",
    categoria: "marco",
    cidade: "Irani",
    uf: "SC",
    endereco: "Rod. SC-468, km 12",
    lat: -27.0270, lng: -51.9020,
    periodo: "1912",
    resumo: "Sítio do primeiro combate da Guerra do Contestado.",
    descricao: "Em 22 de outubro de 1912, neste descampado entre os campos de Irani, deu-se o primeiro confronto armado da Guerra do Contestado, entre a Polícia Militar paranaense e os caboclos liderados pelo monge José Maria. Morreu o monge, morreu o coronel João Gualberto. O sítio preserva a sepultura coletiva e abriga monumento, museu e centro de pesquisa que mantêm vivas as questões agrárias, religiosas e identitárias do conflito.",
    imagens: [["#5a3a2a","#2a1a0e"],["#7a5a4a","#4a3a2a"],["#3a2a1a","#1a0e08"]]
  },
  {
    id: 7,
    nome: "Casa de Cultura Italiana",
    categoria: "casarao",
    cidade: "Concórdia",
    uf: "SC",
    endereco: "Rua Marechal Deodoro, 856 — Centro",
    lat: -27.2340, lng: -52.0270,
    periodo: "1928",
    resumo: "Casarão em madeira que abriga acervo da imigração italiana.",
    descricao: "Construído em 1928 em técnica de tabuado vertical típica das primeiras casas de colonos italianos do meio-oeste catarinense, o casarão foi restaurado nos anos 2000 e abriga hoje a Casa de Cultura Italiana. O acervo reúne mobiliário, documentos, fotografias, instrumentos de trabalho e registros orais de famílias migrantes que se estabeleceram na região a partir da segunda década do século XX.",
    imagens: [["#8a4a2a","#4a2a1a"],["#a06a4a","#6a3a2a"],["#c08a6a","#8a5a3a"]]
  },
  {
    id: 8,
    nome: "Sítio Arqueológico Pré-Colonial Rio Uruguai",
    categoria: "ruina",
    cidade: "Itá",
    uf: "SC",
    endereco: "Margens do Rio Uruguai — Itá Antiga",
    lat: -27.2540, lng: -52.3220,
    periodo: "Pré-1500 / submerso 1999",
    resumo: "Vestígios guaranis e jê às margens do Uruguai, parte submerso pela UHE Itá.",
    descricao: "Antes da formação do reservatório da UHE Itá em 1999, equipes do IPHAN e de universidades parceiras documentaram dezenas de sítios pré-coloniais nas margens do Rio Uruguai — registros de ocupação guarani e de tradição jê com cerâmica, pontas líticas e estruturas semi-subterrâneas. Parte do material foi resgatada e segue em pesquisa; parte permanece submersa. O caso é referência para discussões sobre patrimônio, hidrelétricas e populações atingidas.",
    imagens: [["#3a5a6a","#1a2a3a"],["#5a7a8a","#3a5a6a"],["#2a3a4a","#0e1a24"]]
  },
  {
    id: 9,
    nome: "Estação Ferroviária de Marcelino Ramos",
    categoria: "casarao",
    cidade: "Marcelino Ramos",
    uf: "RS",
    endereco: "Rua da Estação, s/n — Centro",
    lat: -27.4640, lng: -51.9080,
    periodo: "1910",
    resumo: "Antiga estação da São Paulo–Rio Grande, marco da Guerra do Contestado.",
    descricao: "Inaugurada em 1910 como parte da estratégica linha São Paulo–Rio Grande, a estação foi um dos pontos de tensão durante a Guerra do Contestado: por aqui passaram trens militares, suprimentos e correspondência da campanha contra os caboclos sertanejos. O prédio em estilo eclético foi restaurado e abriga acervo ferroviário, conectando memória do trabalho ferroviário, colonização dirigida e conflito agrário no vale do Uruguai.",
    imagens: [["#7a5a2a","#4a3a1a"],["#9a7a4a","#6a4a2a"],["#bab09a","#7a6a4a"]]
  },
  {
    id: 10,
    nome: "Museu Histórico Municipal de Cerro Largo",
    categoria: "museu",
    cidade: "Cerro Largo",
    uf: "RS",
    endereco: "Rua Alfredo Schneider, 220 — Centro",
    lat: -28.1480, lng: -54.7380,
    periodo: "Acervo desde 1902",
    resumo: "Imigração alemã e missões redutórias no noroeste gaúcho.",
    descricao: "O museu municipal reúne acervo sobre a Colônia Serro Azul, fundada em 1902 pela Sociedade União Popular (Volksverein) para acolher imigrantes alemães vindos das colônias velhas do Vale do Sinos. Documenta também o substrato anterior — território guarani das antigas missões — e as transformações da fronteira oeste-noroeste do Rio Grande do Sul ao longo do século XX.",
    imagens: [["#4a6a4a","#1a2a1a"],["#6a8a6a","#3a4a3a"],["#8aaa8a","#5a6a5a"]]
  },
  {
    id: 11,
    nome: "Capela de São Roque",
    categoria: "igreja",
    cidade: "Realeza",
    uf: "PR",
    endereco: "Linha São Roque, s/n — Interior",
    lat: -25.7670, lng: -53.5290,
    periodo: "1962",
    resumo: "Pequena capela rural erguida pelos primeiros colonos sudoestinos.",
    descricao: "Erguida em mutirão pelos primeiros colonos da Linha São Roque em 1962, a capela representa o ciclo de ocupação do sudoeste paranaense que se intensifica após a Revolta dos Posseiros de 1957. A arquitetura simples em alvenaria caiada, com altar em madeira de bracatinga, é típica das centenas de capelas rurais que estruturaram a vida comunitária da região e que hoje compõem um circuito de patrimônio religioso afetivo.",
    imagens: [["#9a8a6a","#5a4a2a"],["#bab09a","#7a6a4a"],["#dad0ba","#9a8a6a"]]
  },
  {
    id: 12,
    nome: "Memorial da Revolta dos Posseiros",
    categoria: "marco",
    cidade: "Francisco Beltrão",
    uf: "PR",
    endereco: "Praça Eduardo Virmond Suplicy — Centro",
    lat: -26.0810, lng: -53.0550,
    periodo: "1957 / memorial 2007",
    resumo: "Marco da resistência camponesa no sudoeste do Paraná.",
    descricao: "Em outubro de 1957, posseiros do sudoeste do Paraná pegaram em armas contra a Companhia CITLA, que tentava expulsá-los das terras já ocupadas. O movimento, articulado entre Francisco Beltrão, Pato Branco e cidades vizinhas, conseguiu reverter o processo e levou à criação do GETSOP, garantindo a titulação das posses. O memorial inaugurado em 2007 reúne painéis, esculturas e arquivo oral que mantêm viva a memória do levante.",
    imagens: [["#8a3a2a","#4a1a0e"],["#aa5a3a","#6a2a1a"],["#caaaa0","#8a5a4a"]]
  },
  {
    id: 13,
    nome: "Casa do Imigrante Polonês",
    categoria: "casarao",
    cidade: "Áurea",
    uf: "RS",
    endereco: "RS-211, km 4 — Linha Cândido Godói",
    lat: -27.7080, lng: -52.0480,
    periodo: "1911",
    resumo: "Casa em troncos encavilhados, modelo da imigração polonesa do Alto Uruguai.",
    descricao: "Áurea concentra a maior comunidade de descendentes poloneses do Brasil. A Casa do Imigrante, restaurada em 1996, é um exemplar da técnica construtiva em troncos encavilhados (sem pregos) trazida pelos colonos que chegaram a partir de 1911. O acervo interno reproduz o cotidiano doméstico, os utensílios e o trabalho agrícola dos primeiros tempos, e dá suporte a um circuito de turismo de memória que envolve dezenas de propriedades vizinhas.",
    imagens: [["#6a4a2a","#3a2a1a"],["#8a6a4a","#5a3a2a"],["#aa8a6a","#7a5a3a"]]
  },
  {
    id: 14,
    nome: "Centro Histórico de Laranjeiras do Sul",
    categoria: "casarao",
    cidade: "Laranjeiras do Sul",
    uf: "PR",
    endereco: "Rua XV de Novembro — Centro",
    lat: -25.4070, lng: -52.4170,
    periodo: "Final séc. XIX",
    resumo: "Antiga capital do Território Federal do Iguaçu (1943–1946).",
    descricao: "Conhecida como antiga \"Vila do Iguaçu\", Laranjeiras do Sul foi sede do efêmero Território Federal do Iguaçu, criado em 1943 e dissolvido em 1946. O centro preserva edifícios públicos do período territorial, casarões em madeira do ciclo da erva-mate e marcos da rota tropeira que ligava Palmas a Guarapuava. É lugar privilegiado para se discutir a fronteira como construção administrativa e disputada do Estado brasileiro.",
    imagens: [["#5a6a4a","#2a3a1a"],["#7a8a6a","#4a5a3a"],["#9aaa8a","#6a7a5a"]]
  }
];

var CATEGORIAS = [
  { id: "todos",   label: "Todos",      icon: "M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" },
  { id: "forte",   label: "Fortes",     icon: "M3 21V8l9-5 9 5v13H3zm6 0v-7h6v7" },
  { id: "ruina",   label: "Ruínas",     icon: "M4 21V10l4-3 4 3v3l4-2 4 2v8H4zm4 0v-5h2v5m6 0v-4h2v4" },
  { id: "museu",   label: "Museus",     icon: "M3 21h18M5 21V10M9 21V10M13 21V10M17 21V10M19 21V10M2 10h20L12 3 2 10z" },
  { id: "igreja",  label: "Igrejas",    icon: "M12 2v4m-2 0h4M5 21V11l7-4 7 4v10H5zm5 0v-5h4v5M11 11h2" },
  { id: "marco",   label: "Marcos",     icon: "M12 22s8-9 8-14a8 8 0 10-16 0c0 5 8 14 8 14zm0-11a3 3 0 100-6 3 3 0 000 6z" },
  { id: "casarao", label: "Casarões",   icon: "M3 11l9-7 9 7v10H3V11zm6 10v-6h6v6" }
];

var CATEGORIA_COR = {
  forte:   "#8a3a2a",
  ruina:   "#7a5a2a",
  museu:   "#1f4a8f",
  igreja:  "#5a3a7a",
  marco:   "#0b2545",
  casarao: "#2d6a4f"
};
