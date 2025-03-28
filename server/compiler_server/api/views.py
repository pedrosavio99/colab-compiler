# api/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .compiler.lexer import lexer as compiler_lexer
from .compiler.parser import parse as compiler_parse
from .compiler.generator import generate_systemverilog
from .compilerSysLogPy.lexer import lexer as syslog_lexer
from .compilerSysLogPy.parser import parse as syslog_parse
from .compilerSysLogPy.generator import generate_python

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, World!'})

@api_view(['POST'])
def compile_code(request):
    try:
        code = request.data.get('code', '')
        if not code:
            return Response({'error': 'Nenhum código fornecido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Tokenização
        tokens = compiler_lexer(code)

        # Parsing
        ast = compiler_parse(tokens)

        # Geração de SystemVerilog
        sv_code = generate_systemverilog(ast)
        
        print(sv_code)

        return Response({
            'tokens': tokens,
            'ast': str(ast),
            'systemverilog': sv_code
        }, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f"Erro interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def compiler_syslog_py(request):
    try:
        code = request.data.get('code', '')
        if not code:
            return Response({'error': 'Nenhum código fornecido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Tokenização
        tokens = syslog_lexer(code)

        # Parsing
        ast = syslog_parse(tokens)

        # Geração de Python
        py_code = generate_python(ast)
        
        print(py_code)

        return Response({
            'tokens': tokens,
            'ast': str(ast),
            'python': py_code
        }, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f"Erro interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)