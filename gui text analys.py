import string  # مكتبة للتعامل مع علامات الترقيم
from customtkinter import * # مكتبة لصناعة واجهة رسوم جميلة
from PIL import Image # مكتبة لقرائة الصور

class gui_window(CTk): # كلاس صناعة واجهة الرسوم
    def __init__(self,titlee="Welcome"): # مقدمة الكائن
        super().__init__()
        self.title(titlee) # اسم النافذة
        self.resizable(False,False) # تقييد الحجم
        self.maincolor = '#05d7ff' # اللون الأساسي
        self.hovercolor = '#037b91' # اللون الفرعي
        set_appearance_mode("dark") # المود المظلم
        '''استعراض الصور'''
        self.count_image = Image.open("images/login dark.png")
        self.search_image = Image.open("images/search dark.png")
        self.exit_image = Image.open("images/Exit Dark.png")
        self.team = CTkLabel( # أسم الفريق
            self,
            text="Go",
            font=("Arial", 30),
            )
        self.text_label = CTkLabel( # ارشاد لوضع الجملة
            self,
            text="Enter text here:",
            font=("Arial", 18),
            )
        self.text_entry = CTkTextbox( # مكان وضع الجملة
            self,
            font=("Arial", 12),
            border_color=self.maincolor,
            border_width=2,
            )
        self.result_label = CTkLabel( # نتيجة التحليل
            self,
            text="",
            font=("Arial", 18),
            )
        self.text_button = CTkButton( # زر التحليل
            self,
            text="Count",
            font=("Arial", 14),
            fg_color='transparent',
            hover_color=self.hovercolor,
            border_color=self.maincolor,
            border_width=2,
            image=CTkImage(dark_image=self.count_image),
            command=self.display_results,
            )
        '''وضع كل عنصر في مكانه'''
        self.columnconfigure(0, weight=1, minsize=100)
        self.columnconfigure(1, weight=1, minsize=100)
        self.columnconfigure(2, weight=1, minsize=100)
        self.columnconfigure(3, weight=1, minsize=100)
        self.team.grid(row=0, column=0, padx=10, pady=10)
        self.text_label.grid(row=1, column=0, padx=10, pady=10)
        self.text_entry.grid(row=1, column=1, padx=10, pady=10)
        self.text_button.grid(row=2, column=0, padx=10, pady=10)
        self.result_label.grid(row=1, column=2, padx=10, pady=10)
    def display_results(self): # دالة لإستعراض نتيجة التحليل
        result_text = self.text_entry.get("1.0", "end-1c") # متغير استدعاء الجمل
        lol=f'''\n--- Text Analysis Results ---\n
Total Characters: {count_characters(result_text)}
Total Words: {count_words(result_text)}
Total Sentences: {count_sentences(result_text)}\n\n--- Word Frequencies ---\n\n'''
        frequencies = word_frequencies(result_text)  # حساب تكرار الكلمات
        for word, freq in frequencies.items(): # الكشف عن التكرار
            lol += f"{word}: {freq}\n" # وضع النتائج في متغير استدعاء الجمل
        self.result_label.configure(text=lol) # تعديل نص النتيجة
        self.search_word=CTkEntry( # مدخل للبحث
            self,
            font=("Arial", 12),
            border_color=self.maincolor,
            border_width=2,
        )
        self.search_word.grid(row=2, column=1, padx=10, pady=10)
        self.search_button = CTkButton( # زر البحث
            self,
            text="Search",
            font=("Arial", 14),
            fg_color='transparent',
            hover_color=self.hovercolor,
            border_color=self.maincolor,
            border_width=2,
            image=CTkImage(dark_image=self.search_image),
            command=self.search_button_func,
            )
        self.search_button.grid(row=2, column=2, padx=10, pady=10)
    def search_button_func(self): # دالة للبحث
        self.searched_word_lable=CTkLabel( # نتيجة البحث
            self,
            text="",
            font=("Arial", 18),
            )
        result_text = self.text_entry.get("1.0", "end-1c") # إستدعاء الجملة
        searched_word = self.search_word.get() # إستدعاء البحث
        positions = find_word_positions(result_text, searched_word)  # البحث عن مواقع الكلمة
        if positions:
            self.searched_word_lable.configure(text=f"The word '{searched_word}' was found at positions: {positions}")
        else:
            self.searched_word_lable.configure(text=f"The word '{searched_word}' was not found in the text.")
        self.searched_word_lable.grid(row=1, column=3, padx=10, pady=10)
        self.exitt = CTkButton( # زر الخروج
            self,
            text="Exit",
            font=("Arial", 14),
            fg_color='transparent',
            hover_color=self.hovercolor,
            border_color=self.maincolor,
            border_width=2,
            command=self.destroy,
            image=CTkImage(dark_image=self.exit_image),
        )
        self.exitt.grid(row=2, column=3, padx=10, pady=10)



app=gui_window("Go Project") # إنشاء الكائن ووضع إسم مخصص للنافذة


# Function to count the number of characters in the text
def count_characters(text):
    """Count the total number of characters in the text."""
    return len(text)  # تحسب طول النص بالأحرف (بما في ذلك الفراغات)

# Function to count the number of words in the text
def count_words(text):
    """Count the total number of words in the text."""
    words = text.split()  # تقسيم النص إلى كلمات بناءً على الفراغات
    return len(words)  # تحسب عدد الكلمات

# Function to count the number of sentences in the text
def count_sentences(text):
    """Count the total number of sentences in the text."""
    sentences = text.split('.')  # تقسيم النص إلى جمل بناءً على النقاط
    return len([s for s in sentences if s.strip() != ""])  # تجاهل الفراغات

# Function to calculate word frequencies
def word_frequencies(text):
    """Calculate the frequency of each word in the text."""
    words = text.lower().translate(str.maketrans("", "", string.punctuation)).split()
    # تحويل النص إلى أحرف صغيرة وحذف علامات الترقيم
    frequency = {}  # قاموس لتخزين تكرار الكلمات
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency  # إرجاع القاموس النهائي

# Function to find positions of a specific word in the text
def find_word_positions(text, search_word):
    """Find positions of a word in the text."""
    words = text.split()  # تقسيم النص إلى كلمات
    positions = [i+1 for i, word in enumerate(words) if word.lower() == search_word.lower()]
    # البحث عن مواقع الكلمة المطلوبة (تجاهل حالة الأحرف)
    return positions

# --- Main Program ---
if __name__ == "__main__": # تشغيل المشروع
    app.mainloop()