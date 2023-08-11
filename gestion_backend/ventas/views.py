from rest_framework.views import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema
from .models import OrderDetails
from .serializers import OrderDetailsSerializer

class OrderViewset(ViewSet):
    @swagger_auto_schema(operation_description="Obtener todas las ordenes de compra.")
    def list(self, request):
        orders = OrderDetails.objects.all()
        serializer = OrderDetailsSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Obtener una orden de compra.")
    def retrieve(self, request, pk=None):
        """
        Obtiene los detalles de una orden de compra específica según su ID.
        Parámetros:
        - pk (int): ID de la orden de compra.

        Respuestas posibles:
        - Éxito:
            - Código de estado: 200
            - Contenido: Detalles de la orden de compra.
        - No encontrado:
            - Código de estado: 404
            - Contenido: {'error': 'Orden no encontrada.'}

        """
        try:
            order = OrderDetails.objects.get(pk=pk)
        except OrderDetails.DoesNotExist:
            return Response({'error': 'Orden no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderDetailsSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Create
    @swagger_auto_schema(operation_description="Crear orden de compra.")
    def create(self, request):
        """
        Crea una nueva orden de compra.
        Parámetros:
        - orderdetails_set (list): Lista de items de la orden con productos y cantidades.

        Respuestas posibles:
        - Éxito:
            - Código de estado: 201
            - Contenido: {'message': 'Orden creada con éxito.'}
        - Errores de validación:
            - Código de estado: 400
            - Contenido: Errores de validación del serializador.
        - Errores de stock:
            - Código de estado: 409
            - Contenido: {'errors': [lista de errores de stock]}
        """
        serializer = OrderDetailsSerializer(data = request.data)
        if serializer.is_valid():
            order_data = serializer.validated_data
            order_items = order_data.get('orderdetails_set', [])
            errors = validate_stock(order_items)
            
            if errors:
                return Response({'errors': errors}, status=status.HTTP_409_CONFLICT)
            
            serializer.save()
            return Response({'message': 'Orden creada con éxito.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete
    @swagger_auto_schema(operation_description="Eliminar orden de compra.")
    def delete(self, request, pk=None):
        """
        Elimina una orden de compra según su ID.
        Parámetros:
        - pk (int): ID de la orden de compra.
        
        Respuestas posibles:
        - Éxito:
            - Código de estado: 200
            - Contenido: {'message': 'Orden eliminada exitosamente.'}
        - No encontrado:
            - Código de estado: 404
            - Contenido: {'error': 'Orden no encontrada.'}

        """
        try:
            order = OrderDetails.objects.get(pk=pk)
            order.delete()
            return Response({'message': 'Orden eliminada exitosamente.'})
        except OrderDetails.DoesNotExist:
            return Response({'error': 'Orden no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
    #Update
    @swagger_auto_schema(operation_description="Actualizar orden de compra.")
    def update(self, request, pk=None):
        """
        Actualiza una orden de compra según su ID.

        Parámetros:
        - pk (int): ID de la orden de compra.
        - orderdetails_set (list): Lista de items de la orden con productos y cantidades.
        Respuestas posibles:
        - Éxito:
            - Código de estado: 200
            - Contenido: Detalles de la orden de compra actualizada.
        - Errores de validación:
            - Código de estado: 400
            - Contenido: Errores de validación del serializador.
        - Errores de stock:
            - Código de estado: 409
            - Contenido: {'errors': [lista de errores de stock]}
        - No encontrado:
            - Código de estado: 404
            - Contenido: {'error': 'Orden no encontrada.'}

        """
        try:
            order = OrderDetails.objects.get(pk=pk)
        except OrderDetails.DoesNotExist:
            return Response({'error': 'Orden no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderDetailsSerializer(instance=order, data=request.data)

        if serializer.is_valid():
            order_data = serializer.validated_data
            order_items = order_data.get('orderdetails_set', [])
            errors = validate_stock(order_items)

            if errors:
                return Response({'errors': errors}, status=status.HTTP_409_CONFLICT)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #List con filtrado
    @swagger_auto_schema(operation_description="Filtrar ordenes de compra.")
    def filter_list(self, request):
        """
        Filtra las órdenes de compra según el estado y/o la fecha.
        Parámetros de consulta:
        - status (str, opcional): Estado de la orden.
        - date (str, opcional): Fecha de la orden en formato YYYY-MM-DD.

        Respuesta exitosa:
        - Código de estado: 200
        - Contenido: Lista de órdenes de compra filtradas.

        """
        status_filter = request.query_params.get('status', None)
        date_filter = request.query_params.get('date', None)

        orders = OrderDetails.objects.all()
        if status_filter:
            orders = orders.filter(status=status_filter)
        if date_filter:
            orders = orders.filter(date=date_filter)

        serializer = OrderDetailsSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
def validate_stock(order_items):
    """
    Realiza la validación del stock para los items de una orden de compra.
    Parámetros:
    - order_items (list): Lista de items de la orden.
    Retorna:
    - Lista de errores de stock.
    """
    errors = []
    
    for order_item in order_items:
        product = order_item['product']
        quantity = order_item['quantity']

        if product.stock < quantity:
            errors.append(f'Stock insuficiente para {product.name}. Cantidad requerida: {quantity}. Stock disponible: {product.stock}')
    
    return errors
