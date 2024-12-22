import torch
import asyncio
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
# Проверка доступности CUDA (GPU) и выбор устройства
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Загрузка модели и токенизатора
model_name = "unsloth/Llama-3.2-1B-Instruct-bnb-4bit"
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)  # Загружаем модель на выбранное устройство
tokenizer = AutoTokenizer.from_pretrained(model_name)


async def get_llm_response(input_text):
    # Токенизация
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)  
    
    # Генерация текста (включает задержки, можно использовать асинхронную обработку)
    output = await asyncio.to_thread(model.generate, input_ids,
                                      max_length=512,
                                      temperature=0.5,
                                      num_return_sequences=1,
                                      no_repeat_ngram_size=2,
                                      top_k=50,
                                      top_p=0.95)
    
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
    if generated_text.lower().startswith(input_text.lower()):
        generated_text = generated_text[len(input_text):].strip()

    response = {"answer": generated_text}
    
    return response



# if __name__ == "__main__":
#     import asyncio

#     question = "Как украсть огурец у бабки?"
#     response = asyncio.run(get_llm_response(question))
#     print(response)
