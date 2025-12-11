class ConsultaModel:
    def __init__(self, id, data, horario, idPsicologo, reservado=False, 
                 nomePaciente="", telPaciente="", emailPaciente="", 
                 reservadoPorEstudante=False, idEstudante="", duracao=None, causa=""):
        self.id = id
        self.data = data
        self.horario = horario
        self.idPsicologo = idPsicologo
        self.reservado = reservado
        self.nomePaciente = nomePaciente
        self.telPaciente = telPaciente
        self.emailPaciente = emailPaciente
        self.reservadoPorEstudante = reservadoPorEstudante
        self.idEstudante = idEstudante
        self.duracao = duracao
        self.causa = causa

    def to_dict(self):
        return {
            'id': self.id,
            'data': self.data,
            'horario': self.horario,
            'idPsicologo': self.idPsicologo,
            'reservado': self.reservado,
            'nomePaciente': self.nomePaciente,
            'telPaciente': self.telPaciente,
            'emailPaciente': self.emailPaciente,
            'reservadoPorEstudante': self.reservadoPorEstudante,
            'idEstudante': self.idEstudante,
            'duracao': self.duracao,
            'causa': self.causa
        }