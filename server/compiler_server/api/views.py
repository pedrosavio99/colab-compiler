from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .compilerwithmodules.pipeline import run_compiler_pipeline  # Import relativo

@api_view(['POST'])
def compiler_syslog_py(request):
    try:
        code = request.data.get('code', '')
        if not code:
            return Response({'error': 'Nenhum código fornecido.'}, status=status.HTTP_400_BAD_REQUEST)

        result = run_compiler_pipeline(code)
        return Response(result, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f"Erro interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)