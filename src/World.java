import java.util.ArrayList;

/**
 * Simulates a world of agents, cops and patches.
 */
class World implements Tickable {
    /**
     * All patches.
     */
    private PatchManager patchManager;

    /**
     * All turtles.
     */
    private ArrayList<Turtle> turtles;

    /**
     * Construct a new World object.
     */
    World() {
        patchManager = new PatchManager();
        turtles = new ArrayList<>();

        for (int i=0; i<Params.NUM_COP(); i++) {
            turtles.add(new Cop(this));
        }

        for (int i=0; i<Params.NUM_AGENT(); i++) {
            turtles.add(new Agent(this));
        }
    }

    /**
     * Get the patch manager.
     * @return the patch manager
     */
    PatchManager getPatchManager() {
        return patchManager;
    }

    /**
     * Update the world.
     */
    @Override
    public void update() {
        patchManager.update();
        turtles.forEach(Turtle::update);
    }
}
