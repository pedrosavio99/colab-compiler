from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .compiler.lexer import lexer
from .compiler.parser import parse
from .compiler.generator import generate_systemverilog

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello World"})

@api_view(['POST'])
def compile_code(request):
    try:
        code = request.data.get('code', '')
        if not code:
            return Response(
                {"error": "Nenhum código fornecido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        tokens = lexer(code)
        ast = parse(tokens)
        sv_code = generate_systemverilog(ast)
        
        print(sv_code)

        return Response({
            "tokens": tokens,
            "ast": str(ast),
            "systemverilog": sv_code
        }, status=status.HTTP_200_OK)

    except SyntaxError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": f"Erro interno: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )