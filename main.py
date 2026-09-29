from chatbot import ChatbotCine

def main():
    bot = ChatbotCine()
    
    print("Escribe 'salir' para terminar la conversación.")
    print("-" * 40)

    while True:
        texto = input("Tú: ")
        
        if texto.lower().strip() in ["salir", "exit", "quit"]:
            print("Bot: ¡Hasta pronto!")
            break
        
        respuesta = bot.procesar_entrada(texto)
        print(f"Bot: {respuesta}")
        print("-" * 40)

if __name__ == "__main__":
    main()