import draw_rna.svg as svg
import re, random, math
import numpy as np

class RNATreeNode:

    def __init__(self):
        self.children_ = []
        self.is_pair_ = False
        self.index_a_ = -1
        self.index_b_ = -1
        self.x_ = 0
        self.y_ = 0
        self.go_x_ = 0
        self.go_y_ = 0

def get_pairmap_from_secstruct(secstruct):
    """
    generates dictionary containing pair mappings

    args:
    secstruct contains secondary structure string

    returns:
    dictionary with pair mappings
    """
    pair_stack = []
    end_stack = []
    pairs_array = []
    i_range = list(range(0,len(secstruct)))

    # initialize all values to -1, meaning no pair
    for ii in i_range:
        pairs_array.append(-1)

    # assign pairs based on secstruct
    for ii in i_range:
        if(secstruct[ii] == "("):
            pair_stack.append(ii)
        elif(secstruct[ii] == ")"):
            if not pair_stack:
                end_stack.append(ii)
            else:
                index = pair_stack.pop()
                pairs_array[index] = ii
                pairs_array[ii] = index
    if len(pair_stack) == len(end_stack):
        n = len(pair_stack)
        for ii in range(n):
            pairs_array[pair_stack[ii]] = end_stack[-ii]
            pairs_array[end_stack[-ii]] = pair_stack[ii]
    else:
         print("ERROR: pairing incorrect %s" % secstruct)

    return pairs_array


def add_nodes_recursive(bi_pairs, rootnode, start_index, end_index):

    if(start_index > end_index) :
        print("Error occured while drawing RNA %d %d" % (start_index, end_index))
        sys.exit(0)

    if(bi_pairs[start_index] == end_index) :

        newnode = RNATreeNode()
        newnode.is_pair_ = True
        newnode.index_a_ = start_index
        newnode.index_b_ = end_index

        add_nodes_recursive(bi_pairs, newnode, start_index+1, end_index-1)

    else :
        newnode = RNATreeNode()
        jj = start_index
        while jj <= end_index:
            if(bi_pairs[jj] > jj) :
                add_nodes_recursive(bi_pairs,newnode, jj, bi_pairs[jj])
                jj = bi_pairs[jj] + 1
            else :
                newsubnode = RNATreeNode()
                newsubnode.is_pair_ = False
                newsubnode.index_a_ = jj
                newnode.children_.append(newsubnode)
                jj += 1

    rootnode.children_.append(newnode)

def setup_coords_recursive(rootnode, parentnode, start_x, start_y, go_x, go_y, NODE_R, PRIMARY_SPACE, PAIR_SPACE, external_multiplier, external_offset):

    cross_x = -go_y
    cross_y = go_x

    children_width = len(rootnode.children_) * NODE_R * 2

    #print('children_width', children_width)

    rootnode.go_x_ = go_x
    rootnode.go_y_ = go_y

    if(len(rootnode.children_) == 1):
        rootnode.x_ = start_x
        rootnode.y_ = start_y

        if(rootnode.children_[0].is_pair_):
            setup_coords_recursive(rootnode.children_[0], rootnode, start_x + go_x * PRIMARY_SPACE, start_y + go_y * PRIMARY_SPACE, go_x, go_y, NODE_R, PRIMARY_SPACE, PAIR_SPACE, external_multiplier, external_offset)
        elif(rootnode.children_[0].is_pair_ == False and rootnode.children_[0].index_a_ < 0):
            setup_coords_recursive(rootnode.children_[0], rootnode, start_x, start_y, go_x, go_y, NODE_R, PRIMARY_SPACE, PAIR_SPACE, external_multiplier, external_offset)
        else:
            setup_coords_recursive(rootnode.children_[0], rootnode, start_x + go_x * PRIMARY_SPACE, start_y + go_y * PRIMARY_SPACE, go_x, go_y, NODE_R, PRIMARY_SPACE, PAIR_SPACE, external_multiplier, external_offset)

    elif(len(rootnode.children_) > 1) :

        npairs = 0
        for ii in range(0, len(rootnode.children_)):
            if(rootnode.children_[ii].is_pair_) :
                npairs+=1

        circle_length = (len(rootnode.children_) + 1) * PRIMARY_SPACE + (npairs + 1) * PAIR_SPACE
        circle_radius = circle_length / (2 * math.pi)

        length_walker = PAIR_SPACE / 2.0

        if (parentnode == None) :
            rootnode.x_ = go_x * circle_radius
            rootnode.y_ = go_y * circle_radius
            circle_radius *= external_multiplier
        else :
            rootnode.x_ = parentnode.x_ + go_x * circle_radius
            rootnode.y_ = parentnode.y_ + go_y * circle_radius

        for ii in range(0,len(rootnode.children_)):

            if (parentnode ==None):

                length_walker += PRIMARY_SPACE

                if(rootnode.children_[ii].is_pair_) :
                    length_walker += PAIR_SPACE / 2.0

                rad_angle = length_walker/circle_length * 2 * math.pi / external_multiplier - math.pi / 2.0 + external_offset
                child_x = rootnode.x_ + math.cos(rad_angle) * cross_x * circle_radius + math.sin(rad_angle) * go_x * circle_radius
                child_y = rootnode.y_ + math.cos(rad_angle) * cross_y * circle_radius + math.sin(rad_angle) * go_y * circle_radius

                child_go_x = child_x - rootnode.x_
                child_go_y = child_y - rootnode.y_
                child_go_len = math.sqrt(child_go_x * child_go_x + child_go_y * child_go_y)

                setup_coords_recursive(rootnode.children_[ii], rootnode, child_x, child_y, child_go_x / child_go_len, child_go_y / child_go_len, NODE_R, PRIMARY_SPACE, PAIR_SPACE, external_multiplier, external_offset)

                if(rootnode.children_[ii].is_pair_) :
                    length_walker += PAIR_SPACE / 2.0

            else:

                length_walker += PRIMARY_SPACE

                if(rootnode.children_[ii].is_pair_) :
                    length_walker += PAIR_SPACE / 2.0

                rad_angle = length_walker/circle_length * 2 * math.pi - math.pi / 2.0
                child_x = rootnode.x_ + math.cos(rad_angle) * cross_x * circle_radius + math.sin(rad_angle) * go_x * circle_radius
                child_y = rootnode.y_ + math.cos(rad_angle) * cross_y * circle_radius + math.sin(rad_angle) * go_y * circle_radius

                child_go_x = child_x - rootnode.x_
                child_go_y = child_y - rootnode.y_
                child_go_len = math.sqrt(child_go_x * child_go_x + child_go_y * child_go_y)

                setup_coords_recursive(rootnode.children_[ii], rootnode, child_x, child_y, child_go_x / child_go_len, child_go_y / child_go_len, NODE_R, PRIMARY_SPACE, PAIR_SPACE, external_multiplier, external_offset)

                if(rootnode.children_[ii].is_pair_) :
                    length_walker += PAIR_SPACE / 2.0

    else :
        rootnode.x_ = start_x
        rootnode.y_ = start_y

def get_coords_recursive(rootnode, xarray, yarray, PRIMARY_SPACE, PAIR_SPACE):
    if(rootnode.is_pair_) :
        cross_x = -rootnode.go_y_
        cross_y = rootnode.go_x_

        xarray[rootnode.index_a_] = rootnode.x_ + cross_x * PAIR_SPACE/2.0
        xarray[rootnode.index_b_] = rootnode.x_ - cross_x * PAIR_SPACE/2.0

        yarray[rootnode.index_a_] = rootnode.y_ + cross_y * PAIR_SPACE/2.0
        yarray[rootnode.index_b_] = rootnode.y_ - cross_y * PAIR_SPACE/2.0
    elif(rootnode.index_a_ >= 0) :
        xarray[rootnode.index_a_] = rootnode.x_
        yarray[rootnode.index_a_] = rootnode.y_

    for ii in range(0, len(rootnode.children_)):
        get_coords_recursive(rootnode.children_[ii], xarray, yarray, PRIMARY_SPACE, PAIR_SPACE)



class RNARenderer:

    def __init__(self):
        self.root_ = None
        self.xarray_ = None
        self.yarray_ = None
        self.size_ = None

    def setup_tree(self, secstruct, NODE_R,PRIMARY_SPACE, PAIR_SPACE, external_multiplier, external_offset):

        dangling_start = 0
        dangling_end = 0
        bi_pairs = get_pairmap_from_secstruct(secstruct)

        self.NODE_R = NODE_R
        self.root_ = None

        for ii in range(0,len(bi_pairs)):
            if bi_pairs[ii] < 0:
                dangling_start+=1
            else:
                break

        for ii in (len(bi_pairs)-1,-1, -1) :
            if(bi_pairs[ii] < 0):
                dangling_end+=1
            else:
                break

        self.root_ = RNATreeNode()

        #for jj in range(0,len(bi_pairs)):
        jj = 0
        while (jj < len(bi_pairs)):
            if (bi_pairs[jj] > jj) :
                add_nodes_recursive(bi_pairs,self.root_, jj, bi_pairs[jj])
                jj = bi_pairs[jj] + 1
            else:
                newsubnode = RNATreeNode()
                newsubnode.is_pair_ = False
                newsubnode.index_a_ = jj
                self.root_.children_.append(newsubnode)
                jj += 1
        xarray = []
        yarray = []

        for ii in range(0,len(secstruct)):
            xarray.append(0.0)
            yarray.append(0.0)

        self.setup_coords(NODE_R,PRIMARY_SPACE,PAIR_SPACE, external_multiplier, external_offset)
        self.get_coords(xarray,yarray,PRIMARY_SPACE,PAIR_SPACE)

        min_x = xarray[0] - NODE_R
        min_y = yarray[0] - NODE_R
        max_x = xarray[0] + NODE_R
        max_y = xarray[0] + NODE_R

        for x in xarray:
            if x - NODE_R < min_x:
                min_x = x - NODE_R
            if x + NODE_R > max_x:
                max_x = x + NODE_R

        for y in yarray:
            if y - NODE_R < min_y:
                min_y = y - NODE_R
            if y + NODE_R > max_y:
                max_y = y + NODE_R

        for ii in range(0,len(xarray)):
            xarray[ii] -= min_x
            yarray[ii] -= min_y

        self.size_ = [max_x - min_x, max_y - min_y]
        self.xarray_ = xarray
        self.yarray_ = yarray

    def get_size(self):
        return self.size_

    def draw(self, svgobj, offset_x, offset_y, colors, pairs, sequence, render_in_letter, external_offset, line=False, svg_mode=True, alpha=None):
        if alpha is None:
            alpha = np.ones(len(self.xarray_))

        if self.xarray_ != None:

            if line:
                for ii in range(len(self.xarray_)-1):
                    if colors == None:
                        svgobj.line(self.xarray_[ii], self.yarray_[ii], self.xarray_[ii+1], self.yarray_[ii+1],
                                    'black')
                    else:
                        svgobj.line(self.xarray_[ii], self.yarray_[ii], self.xarray_[ii+1], self.yarray_[ii+1],
                                    colors[ii])
            else:
                if pairs:
                    for pair in pairs:
                        svgobj.line(offset_x + self.xarray_[pair['from']], offset_y + self.yarray_[pair['from']],
                         offset_x + self.xarray_[pair['to']], offset_y + self.yarray_[pair['to']],
                          pair['color'], self.NODE_R, alpha=min([alpha[pair['from']],alpha[pair['to']]]))

                for ii in range(0,len(self.xarray_)):
                    if colors == None:
                        svgobj.circle(self.xarray_[ii] + offset_x, self.yarray_[ii] + offset_y, self.NODE_R, "#000000", "#000000", alpha[ii])
                    else:
                        svgobj.circle(self.xarray_[ii] + offset_x, self.yarray_[ii] + offset_y, self.NODE_R, colors[ii], colors[ii], alpha[ii])

                if sequence and render_in_letter:

                    # write 5' 3' markers
                    svgobj.text(self.xarray_[0] + offset_x - math.sin(external_offset)*2.5*self.NODE_R,
                     self.yarray_[0] + offset_y - math.cos(external_offset)* 2.5*self.NODE_R, self.NODE_R * 1.5, "#000000", "center", "5'", 1)

                    svgobj.text(self.xarray_[-1] + offset_x - math.sin(external_offset)*2.5*self.NODE_R,
                     self.yarray_[-1] + offset_y - math.cos(external_offset)* 2.5*self.NODE_R, self.NODE_R * 1.5, "#000000", "center", "3'", 1)

                    for ii in range(0,len(self.xarray_)):
                        text_size = self.NODE_R * 1.5
                        if colors[ii] == [0,0,0]:
                            color = "#FFFFFF"
                        else:
                            color = "#000000"

                        if svg_mode:
                            text_offset_x = -4.0
                            text_offset_y = (text_size)/2.0 - 1.0
                            svgobj.text(self.xarray_[ii] + offset_x + text_offset_x, self.yarray_[ii] + offset_y + text_offset_y, text_size, color, "center", sequence[ii])
                        else:
                            svgobj.text(self.xarray_[ii] + offset_x, self.yarray_[ii] + offset_y, text_size, color, "center", sequence[ii], alpha[ii])

    def get_coords(self, xarray, yarray, PRIMARY_SPACE, PAIR_SPACE):

        if(self.root_ != None) :
            get_coords_recursive(self.root_, xarray, yarray, PRIMARY_SPACE, PAIR_SPACE)
        else :
            for ii in range(0,len(xarray)):
                xarray[ii] = 0
                yarray[ii] = ii * PRIMARY_SPACE

    def setup_coords(self, NODE_R, PRIMARY_SPACE, PAIR_SPACE, external_multiplier, external_offset):
        if self.root_ != None:
            setup_coords_recursive(self.root_, None, 0, 0, 0, 1, NODE_R, PRIMARY_SPACE, PAIR_SPACE, external_multiplier, external_offset)



