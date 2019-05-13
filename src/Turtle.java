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
        move();
    }

    /**
     * Move to a random, unoccupied patch.
     */
    private void move() {
        Patch newPatch = world.getPatchManager().getRandomUnoccupiedPatch();
        moveToPatch(newPatch);
    }

    /**
     * Move to a specified patch.
     * @param newPatch the new patch to be moved to
     */
    void moveToPatch(Patch newPatch) {
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
}
