from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class LettersView(View):
    template_name = 'game/letters.html'
    
    def get(self, request):
        user = request.user
        all_letters = []
        with open(f'md/{user.email}/letter.md', 'r') as file:
            letters = file.read()
            number_of_letters = 0
            letter = ''
            for line in letters.split('\n'):
                
                if line.startswith('#'):
                    number_of_letters +=1
                    all_letters.append(letter)
                    letter = ''
                else:
                    letter = letter +line + '\n'
            all_letters.append(letter)
        all_letters.reverse()         
        context = {'all_letters': all_letters, 'number_of_letters': number_of_letters}
        return render(request, 'game/letters.html', context)


class SingleLetterView(View):

    def get(self,request,pk):
        user = request.user
        all_letters = []
        with open(f'md/{user.email}/letter.md', 'r') as file:
            letters = file.read()
            number_of_letters = 0
            letter = ''
            for line in letters.split('\n'):
                
                if line.startswith('#'):
                    number_of_letters +=1
                    all_letters.append(letter)
                    if number_of_letters == pk:
                        letter_title = line[1:].strip()
                    letter = ''
                else:
                    letter = letter +line + '\n'
            all_letters.append(letter)          
        
        context = {'letter': all_letters[pk], 'pk': pk ,'letter_title': letter_title}
        return render(request, 'game/single_letter.html', context)
