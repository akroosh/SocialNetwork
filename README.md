# SocialNetwork
Simple REST API with implemented token authentication

<h2>Getting Started</h2>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3</li>
  <li>pip3 to install dependencies</li>
  <li>PostgreSQL</li>
  </ul>

<h3>Installing packages</h3>
<ol>
 <li>Run <code>virtualenv env</code> to create virtual environment </li>
 <li>Activate it by <code>source env/bin/activate</code></li>
 <li>Run <code>pip3 install -r requirements.txt</code></li>
 </ol>

<h3>Set up database</h3>
<ol>
<li>Open django_network/settings.</li>
<li>Find DATABASES and change configuration credentials.</li>
</ol>

<h3>Start app</h3>
<ol>
<li><code>cd django_network</code></li>
<li><code>python3 manage.py makemigrations</code></li>
<li><code>python3 manage.py migrate</code></li>
<li><code>python3 manage.py runserver</code></li>
</ol>