from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
import os
from pathlib import Path
from markdown2 import Markdown
from accounts.models import Profile
from django.contrib import messages
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

class FileLettersView(View):
    def get(self,request):
        BASE_DIR = Path(__file__).resolve().parent.parent
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse('accounts:login'))
        user_profile = Profile.objects.get(user=user)
        user_xp = user_profile.xp
        user_rank = user_profile.rank
        str_email = str(user.email)
        avatar = str_email[0].capitalize 
        letters_path = Path(BASE_DIR,'md', user.email,'letters')
        letters_count = len([f for f in os.listdir(letters_path) if os.path.isfile(os.path.join(letters_path, f))])
        letters = os.listdir(letters_path)
        for i in range(len(letters)):
            letters[i] = letters[i][2:-3]

        context = {'letters_count':letters_count ,
                    'letters':letters,
                    'xp':user_xp,
                    'rank':user_rank,
                    'avatar':avatar
                    }
        return render(request, 'game/index.html', context)

class FileSingleLetterView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse('accounts:login'))
        user_profile = Profile.objects.get(user=user)
        user_xp = user_profile.xp
        user_rank = user_profile.rank
        str_email = str(user.email)
        avatar = str_email[0].capitalize
            
        markdowner = Markdown(extras=[
            'fenced-code-blocks',
            'tables',
            'header-ids',
            'break-on-newline',
            'task_list',
            'footnotes'
        ])
        
        BASE_DIR = Path(__file__).resolve().parent.parent
        letters_path = Path(BASE_DIR, 'md', user.email, 'letters')
        
        try:
            # Find the correct letter file
            letter_name = None
            for file in letters_path.iterdir():
                if file.stem.startswith(f'{pk}.'):
                    letter_name = file
                    break
                    
            if letter_name is None:
                return redirect(reverse('game:file_letters'))
                
            # Read and convert the letter
            letter_content = letter_name.read_text(encoding='utf-8')
            html_content = markdowner.convert(letter_content)
            letter_name = str(letter_name)
            last_index = letter_name.rindex(str(BASE_DIR))
            letter_name= letter_name[last_index + len(str(BASE_DIR))+15+len(str(user.email)):-3]
            context = {
                'letter': html_content,
                'letter_title': letter_name,
                'xp':user_xp,
                'rank':user_rank,
                'avatar':avatar
            }
            return render(request, 'game/letter.html', context)
            
        except (FileNotFoundError, PermissionError) as e:
            messages.error(request,'نامه مورد نظر پیدا نشد')
            return redirect(reverse('game:file_letters'))
    def post(self,request,pk):
        user = request.user
        user_profile = Profile.objects.get(user=user)
        user_profile.xp +=200
        user_profile.save()
        letter_name = None
        BASE_DIR = Path(__file__).resolve().parent.parent
        letters_path = Path(BASE_DIR, 'md', user.email, 'letters')
        for file in letters_path.iterdir():
            if file.stem.startswith(f'{pk}.'):
                letter_name = file
                break
                    
        if letter_name is None:
            return redirect(reverse('game:file_letters'))
        with open(letter_name , 'a', encoding='utf-8') as file:
            text = '\n' +'\n'+'---' +'\n' + 'پاسخ شما:' + self.request.POST.get('journal')
            file.write(text)
        messages.success(request, 'پاسخ شما با موفقیت ثبت شد')
        return redirect(reverse('game:file_letters'))

class FileJournalsView(View):
    def get(self,request):
        BASE_DIR = Path(__file__).resolve().parent.parent
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse('accounts:login'))
        user_profile = Profile.objects.get(user=user)
        user_xp = user_profile.xp
        user_rank = user_profile.rank
        str_email = str(user.email)
        avatar = str_email[0].capitalize 
        journals_path = Path(BASE_DIR,'md', user.email,'journals')
        journals_count = len([f for f in os.listdir(journals_path) if os.path.isfile(os.path.join(journals_path, f))])
        journals = os.listdir(journals_path)
        for i in range(len(journals)):
            journals[i] = journals[i][2:-3]

        context = {'letters_count':journals_count ,
                    'letters':journals,
                    'xp':user_xp,
                    'rank':user_rank,
                    'avatar':avatar
                    }
        return render(request, 'game/journals_home.html', context)

class FileSingleJOurnalView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse('accounts:login'))
        user_profile = Profile.objects.get(user=user)
        user_xp = user_profile.xp
        user_rank = user_profile.rank
        str_email = str(user.email)
        avatar = str_email[0].capitalize
            
        markdowner = Markdown(extras=[
            'fenced-code-blocks',
            'tables',
            'header-ids',
            'break-on-newline',
            'task_list',
            'footnotes'
        ])
        
        BASE_DIR = Path(__file__).resolve().parent.parent
        journals_path = Path(BASE_DIR, 'md', user.email, 'journals')
        
        try:
            # Find the correct letter file
            journal_name = None
            for file in journals_path.iterdir():
                if file.stem.startswith(f'{pk}.'):
                    journal_name = file
                    break
                    
            if journal_name is None:
                return redirect(reverse('game:file_journals'))
                
            # Read and convert the letter
            journal_content = journal_name.read_text(encoding='utf-8')
            html_content = markdowner.convert(journal_content)
            journal_name = str(journal_name)
            last_index = journal_name.rindex(str(BASE_DIR))
            journal_name= journal_name[last_index + len(str(BASE_DIR))+16+len(str(user.email)):-3]
            context = {
                'letter': html_content,
                'letter_title': journal_name,
                'xp':user_xp,
                'rank':user_rank,
                'avatar':avatar
            }
            return render(request, 'game/letter.html', context)
            
        except (FileNotFoundError, PermissionError) as e:
            messages.error(request,'نامه مورد نظر پیدا نشد')
            return redirect(reverse('game:file_journals'))

             