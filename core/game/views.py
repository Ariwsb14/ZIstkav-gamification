from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.

class LettersView(View,LoginRequiredMixin):
    template_name = 'game/letters.html'
    
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse('accounts:login'))
        all_letters = []
        all_journals = []
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
            file.close()
        with open(f'md/{user.email}/journal.md', 'r') as file:
            journals = file.read()
            number_of_journals = 0
            journal = ''
            for line in journals.split('\n'):
                if line.startswith('#'):
                    number_of_journals +=1
                    all_journals.append(journal)
                elif line.startswith('your answer:'):
                    continue
                else:
                    journal = journal + line + '\n'
            all_journals.append(journal)
            file.close()
        all_letters.reverse()         
        context = {'all_letters': all_letters, 'number_of_letters': number_of_letters, 
                   'all_journals':all_journals,'number_of_journals':number_of_journals}
        return render(request, 'game/letters.html', context)


class SingleLetterView(View,LoginRequiredMixin):

    def get(self,request,pk):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse('accounts:login'))
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
            file.close()
        context = {'letter': all_letters[pk], 'pk': pk ,'letter_title': letter_title}
        return render(request, 'game/single_letter.html', context)
    
class SingleJournalView(View):
    def get(self,request,pk):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse('accounts:login'))
        all_journals = []
        with open(f'md/{user.email}/journal.md', 'r') as file:
            journals = file.read()
            number_of_journals = 0
            journal = ''
            for line in journals.split('\n'):
                
                if line.startswith('#'):
                    number_of_journals +=1
                    all_journals.append(journal)
                    if number_of_journals == pk:
                        journal_title = line[1:].strip()
                    journal = ''
                elif line.startswith('your answer:'):
                    continue
                else:
                    journal = journal +line + '\n'
            all_journals.append(journal)          
            file.close()
        
        context = {'journal': all_journals[pk], 'pk': pk ,'journal_title': journal_title}
        return render(request, 'game/single_journal.html', context)
    
    def post(self,request,pk):
        user = request.user
        text = self.request.POST.get('text')
        text='your answer: ' + text + '\n'
        numbers_of_journals = 0
        journal_lines = []
        lines = open(f'md/{user.email}/journal.md','r').readlines()
        file = open(f'md/{user.email}/journal.md','w')
        for line in range(len(lines)):
            if lines[line].startswith('#'):
                numbers_of_journals +=1
                journal_lines.append(line)
        print(journal_lines)
        
        if pk == numbers_of_journals:
            lines.append(text)
        else:
            lines.insert(journal_lines[pk],text)
        file.writelines(lines)
        file.close()
        return redirect(reverse('game:letters'))
    