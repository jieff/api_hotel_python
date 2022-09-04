from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.34,
        'cidade': 'São Paulo'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 4.5,
        'diaria': 520.34,
        'cidade': 'Florianopolis'
    },

]



class Hoteis(Resource):

    def get(self):
        return {'hoteis': hoteis}


class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome')
    atributos.add_argument('estrelas')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel ['hotel_id'] == hotel_id:
                return hotel
        return None
    

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):
      
        dados = Hotel.atributos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        

        '''
        novo_hotel = { 'hotel_id': hotel_id, **dados }
        novo_hotel = {
            'hotel_id': hotel_id,
            'nome'    : dados['nome'],
            'estrelas': dados['estrelas'],
            'diarias'  : dados['diarias'],
            'cidade'  : dados['cidade']
        }
        '''

        hoteis.append(novo_hotel)

        return novo_hotel, 200

    def put(self, hotel_id):

        dados = Hotel.atributos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        
        #novo_hotel = { 'hotel_id': hotel_id, **dados }

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200 #success   
        hoteis.append(novo_hotel)
        return novo_hotel, 201 #created

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted.'}