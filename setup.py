from cx_Freeze import setup, Executable
import os
base = None    
os.environ['TCL_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tk8.6'

executables = [Executable("main v2.0.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
		'include_files':[
            os.path.join(r'C:\ProgramData\Anaconda3', 'DLLs', 'tk86t.dll'),
            os.path.join(r'C:\ProgramData\Anaconda3', 'DLLs', 'tcl86t.dll')]
		 },    
}

setup(
    name = "Курсовой проект",
    options = options,
    version = "2.0",
    description = 'Программное обеспечение, ссозданное в рамках курсового проектирования в по дисциплине "Планирование и анализ эксперимента". Предоставляет возможность составления планов эксперимента на нечетких множеств для линейных и квадратичных моделей.',
    executables = executables
)