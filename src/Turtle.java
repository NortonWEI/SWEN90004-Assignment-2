/**
 * Simulates a turtle object. Must be extended to use.
 *
 * @author Dafu Ai
 */
abstract class Turtle implements Tickable {
    /**
     * The patch this turtle is currently at.
     */
    protected Patch patch;

    /**
     * The world this turtle is in.
     */
    protected World world;

    /**
     * Construct a new Turtle instance.
     * @param world world this turtle is in.
     */
    Turtle(World world) {
        this.world = world;

        if (canMove()) {
            move();
        }
    }

    /**
     * Move to a random, unoccupied patch.
     */
    private void move() {
        Patch newPatch = world.getPatchMap().getRandomUnoccupiedPatch();
        moveToPatch(newPatch);
    }

    /**
     * Move to a specified patch.
     * @param newPatch the new patch to be moved to
     */
    void moveToPatch(Patch newPatch) {
        if (patch != null) {
            patch.removeTurtle(this);
        }
        newPatch.addTurtle(this);
        this.patch = newPatch;
    }

    /**
     * Get the current patch.
     * @return the current patch
     */
    Patch getPatch() {
        return patch;
    }

    /**
     * Update the current state
     */
    public void update() {
        move();
    }

    /**
     * Determines whether this turtle can move.
     * @return true if it can; false otherwise
     */
    abstract boolean canMove();
}
