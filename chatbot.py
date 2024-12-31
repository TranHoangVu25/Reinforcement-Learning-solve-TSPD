# To import google.generativeai as genai and use this
# file you must create anaconda environment and call gemeni or another chatbot API
import google.generativeai as genai


def model():
    GOOGLE_API_KEY = "API here"

    try:
        genai.configure(api_key= GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-pro")
        return model
    except Exception as e:
        print(e)
    

def infor():
    user_text = input('Enter your text:')
    model_id = model()
    response = model_id.generate_content(f'Give me the information of the content {user_text}')
    result = response.text
    return result

if __name__ == '__main__':
    infor()

