# Ideas worth considering

- [HalfVoxel2018](https://github.com/HalfVoxel/battlecode2018/blob/master/README.md) Potential rush strategy: Instead of building a factory near our starting position, let a worker go to the enemy and build it there instead. This way we can still build a good economy in the beginning of the game, while still being able to attack the enemy early.

- [CIS 15-466 CMU](http://www.cs.cmu.edu/~maxim/classes/CIS15466_Fall11/lectures/strategy_cis15466.pdf) Tactical Locations (“rally points”) - Points that have important tactical features
    - safe locations for troops to retreat to in case of defeat (commonly used in real-world military planning)
    - cover points (e. g., hiding place behind barrels, etc.)
    - sniper points
    - avoid points (e. g., exposed areas, etc.)
    - shadow points (e. g., out-of-light points)-
    A state is given by true/false for each attribute (cover, shadow, exposure) Two states are connected by transition if they are quickly reachable (and visible)

    Rule for Area of Security : A location (cell) is secure if at least four of its eight neighbors ( 50 % ) are secure. Cellular automata to implement

- [Paper](http://www.csse.uwa.edu.au/cig08/Proceedings/papers/8054.pdf)