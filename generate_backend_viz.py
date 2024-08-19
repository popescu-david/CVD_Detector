import os
from graphviz import Digraph
 
project_name = "CVD_Detector"
apps = ["CVD_Detector", "Users", "Detector"]
 
app_colors = {
    "CVD_Detector": "lightblue",
    "Users": "lightgreen",
    "Detector": "lightcoral"
}
 
dot = Digraph(comment=f'{project_name} Project Structure')
 
dot.attr(size='20,20', pad='0.5,0.5')
dot.attr(rankdir='TB')
dot.attr(splines='true')

dot.node(project_name, project_name, shape='folder', style='filled', color='lightgrey', fontname='Helvetica', fontsize='16', fontcolor='black')

for app in apps:
    dot.node(app, app, shape='folder', style='filled', color=app_colors[app], fontname='Helvetica', fontsize='14', fontcolor='black')
    dot.edge(project_name, app, color='black')

dot.node('AdminSite_CVD', 'Custom Admin Site', shape='ellipse', style='filled, rounded', color=app_colors['CVD_Detector'], fontname='Helvetica', fontsize='12', fontcolor='black')
dot.edge('CVD_Detector', 'AdminSite_CVD', color='black')

user_nodes = {
    'Register_Users': 'Register',
    'Login_Users': 'Login',
    'Logout_Users': 'Logout',
    'PasswordReset_Users': 'Password Reset'
}
for node, label in user_nodes.items():
    dot.node(node, label, shape='ellipse', style='filled, rounded', color=app_colors['Users'], fontname='Helvetica', fontsize='12', fontcolor='black')
    dot.edge('Users', node, color='black')

detector_nodes = {
    'About_Detector': 'About Page',
    'PatientData_Detector': 'Patient Data Pages',
    'HomePage_Detector': 'Home Page'
}
for node, label in detector_nodes.items():
    dot.node(node, label, shape='ellipse', style='filled, rounded', color=app_colors['Detector'], fontname='Helvetica', fontsize='12', fontcolor='black')
    dot.edge('Detector', node, color='black')

output_file = 'backend_visualized'
dot.render(output_file, format='png', cleanup=True)

os.system(f'dot -Tpng -Gdpi=300 {output_file}.dot -o {output_file}.png')
 
print(f'Flow image generated and saved as {output_file}.png')
 