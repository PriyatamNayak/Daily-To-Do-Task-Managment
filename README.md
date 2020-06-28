## Daily-To-Do-Task-Managment
<p><a href="https://python.org/" rel="nofollow"><img src="https://camo.githubusercontent.com/364d2f6ca896e34a655a6d1befbfea9553f850c6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d332e372d627269676874677265656e2e737667" alt="Python Version" data-canonical-src="https://img.shields.io/badge/python-3.7-brightgreen.svg"></a>&nbsp;<a href="https://djangoproject.com/" rel="nofollow"><img src="https://camo.githubusercontent.com/0195f9a2e578ffdfe82ca3f237e278da19a65041/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f646a616e676f2d322e312d627269676874677265656e2e737667" alt="Django Version" data-canonical-src="https://img.shields.io/badge/django-2.1-brightgreen.svg"></a>&nbsp;<a href="https://www.django-rest-framework.org/" rel="nofollow"><img src="https://camo.githubusercontent.com/9e7a0c32ba4dee9a8a54045a3f596248b26b5666/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f646a616e676f726573746672616d65776f726b2d332e392d627269676874677265656e2e737667" alt="Django Rest Framework Version" data-canonical-src="https://img.shields.io/badge/djangorestframework-3.9-brightgreen.svg"></a></p>

Based on Djanago , secure and shareable.  Add daily activities , schedule your activity and add notes to do revision. 
1. Add your notes to keep them fopr future use and you can revise them.
2. Add activities , Schedule activities


# Running the Project Locally

Create pipenv and install all dependencies.
```bash
$ pip install pipenv

$ pipenv install

$ pipenv shell
```
First, clone the repository to your local machine:

### git clone https://github.com/mailtodanish/Daily-To-Do-Task-Managment.git

Install the requirements:

Apply the migrations:

dont forget to load applictaion data.
```bash
python manage.py migrate

python manage.py createsuperuser

python manage.py loaddata ApplictaionData.json
```
Update your Secrate Key in seting.py

Finally, run the development server:

python manage.py runserver


