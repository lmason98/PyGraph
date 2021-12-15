# PyGraph
A GUI graphing tool most useful for visualizing graph theory problems.

## Usage:
* Create a vertex by clicking anywhere on the screen where a vertex does not already exist.
* Create an edge by clicking two different vertices in a row.
* Delete a vertex by selecting one (by clicking, it should become a focused color) then press the backspace or delete key to delete it.
* Delete an edge exactly like deleting a vertex (selecting then backspace/delete), or by deleting a vertex that it is connected to.
* Move a vertex by click (hold) and dragging an existing vertex.

## Note:
The logic behind selecting edges is kind of broken, I went with a vertex point distance algorithm to determine if the 
mouse is hovering over an edge, which is failing miserably. It can be really hard at times to select an edge, ideally
the edge object can be refactored into a pygame sprite so we can use their collision logic which I image will work much
better.

## Required functionality:
- [x] Graphical display of vertices and edges
- [x] Input of vertices and edges
- [x] Able to reposition vertices while maintaining adjacencies
- [x] Deletion of vertices and edges
- [x] Parallel edges
- [x] Ability to label vertices
- [ ] Loops

## Recommended features:
- [x] Information about numbers of vertices and edges
