from setuptools import setup, find_packages

setup(
    name='TodoManager',
    version='0.1',
    description='一个基于Python和PyQt6的现代化任务管理系统',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyQt6',
        'sqlite3',
        # 其他依赖项
    ],
    entry_points={
        'console_scripts': [
            'todo-manager=main:main',  # 假设main.py中有一个main函数
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
