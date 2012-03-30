from flask import Flask, render_template, jsonify
app = Flask(__name__)

dummy_data = [5, 10, 40, 30, 20, 10, 10, 0]

def get_group_pricebands(group):
    return [i*10 for i in dummy_data]

def get_category_pricebands(category):
    return [i*5 for i in dummy_data]

def get_brand_pricebands(brand):
    return [i*20 for i in dummy_data]

def get_brand_cats(brand):
    return [('jumpers', 'Tops', 567), ('shoes', 'Footware', 789), ('jackets', 'Outwear', 45), ('tops', 'Tops', 1234), ('hats', 'Accessories', 100)]

def generate_graph(catgeory_data, brand):
    nodes, links = [], []
    groups, count, group_node_size= {}, 1, 20
    max_size, max_node_size = 0, 20

    #Add main node for the brand
    root_index = 0
    root_group = 0
    root_size = 30
    nodes.append({'name': str(brand), 'size':root_size, 'group': root_group})

    #Generate the group nodes
    for c,g,size in catgeory_data:
        if g not in groups:
            groups[g] = count
            count+=1

        if max_size>size:
            max_size=size

    print groups

    #Generate the links for groups to the brand
    for g, i in groups.iteritems():
        nodes.append({'id': i, 'name':g,'size':group_node_size, 'group': groups[g], 'pricebands': get_group_pricebands(g)})
        links.append({'source':i, 'target':root_index, 'value':1})

    #Generate the nodes and links for the category
    for c,g,size in catgeory_data:
        csize = int(max_node_size *(max_size/size))
        nodes.append({'id': count, 'name':c,'size':10, 'group': groups[g], 'pricebands': get_category_pricebands(g)})
        links.append({'source':count, 'target':groups[g], 'value':1})
        count+=1

    graph = {
        'nodes':nodes, 'links': links, 'brand_prices': get_brand_pricebands(brand)
    }

    return graph
    #return {nodes:{'jumpers' : 78, 'shoes':15, 'jackets':187, 'tops':300}

@app.route('/viz')
def intro(brand=None):
    return render_template('viz_intro.html')

@app.route('/graphs.json/<brand>')
def graphs(brand=None):
    data = generate_graph(get_brand_cats(brand), brand)
    return jsonify(data)

@app.route('/viz/<brand>')
def viz(brand=None):
    data={}
    if brand:
        data = generate_graph(get_brand_cats(brand), brand)
    response={'brand':brand, 'data':data, 'datasize':len(data)}
    print response
    return render_template('viz.html', info=response)

if __name__ == "__main__":
    app.run(debug=True)
