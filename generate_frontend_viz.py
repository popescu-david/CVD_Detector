import os
from graphviz import Digraph
 
template_structure = {
    "Navbar Template": ["Base Template", "Base Admin Template"],
    "Base Template": ["About Page", "Home Page", "Login", "Logout", "Register", "Profile"],
    "Base Admin Template": ["Admin Templates"],
    "Home Page": ["Patient Details"],
    "Login": ["Password Reset"],
    "Password Reset": ["Password Reset Confirm"]
}
 
dot = Digraph(comment='Django Templates Structure')
 
dot.attr(size='20,20', pad='0.5,0.5')
dot.attr(rankdir='TB')
dot.attr(splines='true')

template_colors = {
    "Navbar Template": "lightblue",
    "Base Template": "lightgrey",
    "Base Admin Template": "lightgrey",
    "Admin Templates": "lightcoral",
    "About Page": "lightyellow",
    "Home Page": "lightyellow",
    "Patient Details": "lightyellow",
    "Login": "lightpink",
    "Logout": "lightpink",
    "Register": "lightpink",
    "Profile": "lightpink",
    "Password Reset": "lightpink",
    "Password Reset Confirm": "lightpink"
}

for parent, children in template_structure.items():
    dot.node(parent, parent, shape='box', style='filled, rounded', color=template_colors.get(parent, 'white'), fontname='Helvetica', fontsize='12', fontcolor='black')
    for child in children:
        dot.node(child, child, shape='box', style='filled, rounded', color=template_colors.get(child, 'white'), fontname='Helvetica', fontsize='12', fontcolor='black')
        dot.edge(parent, child, color='black')
 
output_file = 'frontend_visualized'
dot.render(output_file, format='png', cleanup=True)

os.system(f'dot -Tpng -Gdpi=300 {output_file}.dot -o {output_file}.png')
 
print(f'Flowchart generated and saved as {output_file}.png')
 