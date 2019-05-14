import java.util.Random;

/**
 * Simulates an Agent.
 */
public class Agent extends Turtle {
    /**
     * Indicates whether the turtle is open rebelling
     */
    private boolean active;

    /**
     * Remaining time length for jailing
     */
    private int jailTerm;

    /**
     * The degree of reluctance to take risks
     */
    private double riskAversion;

    /**
     * Perceived hardship of rebelling
     */
    private double perceivedHardship;

    /**
     * Construct a new Agent object.
     * @param world the world the agent is in
     */
    Agent(World world) {
        super(world);
        Random r = new Random();
        riskAversion = r.nextDouble();
        perceivedHardship = r.nextDouble();
        active = false;
        jailTerm = 0;
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void update() {
        super.update();

        // Only determine behaviour if it is not jailed
        if (!isJailed()) {
            determineBehaviour();
        }

        decrementJailTerm();
    }

    /**
     * The agent can only move if it's not jailed.
     */
    @Override
    boolean canMove() {
        return !isJailed();
    }

    /**
     * Calculate and return the grievance of the agent.
     * @return the grievance
     */
    private double getGrievance() {
        return perceivedHardship * (1 - Params.GOVERNMENT_LEGITIMACY);
    }

    /**
     * Calculate and return the estimated arrest probability of the agent.
     * @return the probability
     */
    private double getEstimatedArrestProbability() {
        PatchManager patchManager = world.getPatchManager();
        int c = patchManager.getNeighbourTurtleCount(patch, Cop.class, null);
        int a = 1 + patchManager.getNeighbourTurtleCount(patch, Agent.class, (turtle -> ((Agent) turtle).active));
        return 1 - Math.exp(-Params.K*Math.floor(c/a));
    }

    /**
     * Determine the behaviour of this agent by flagging its activeness.
     */
    public void determineBehaviour() {
        this.active = (getGrievance() - riskAversion * getEstimatedArrestProbability()) > Params.THRESHOLD;
    }

    /**
     * Determine whether this agent is currently jailed.
     * @return true if jailed; false otherwise
     */
    boolean isJailed() {
        return jailTerm > 0;
    }

    /**
     * Start a new jail term.
     * @param jailTerm the time duration for jailing
     */
    void setJailTerm(int jailTerm) {
        this.jailTerm = jailTerm;
    }

    /**
     * Decrement the current jail term.
     */
    private void decrementJailTerm() {
        if (jailTerm > 0) {
            jailTerm -= 1;
        }
    }

    /**
     * Get activeness of the patch.
     * @return true if active; false otherwise.
     */
    boolean isActive() {
        return active;
    }

    /**
     * Set activeness of the patch.
     */
    void setActive(boolean active) {
        this.active = active;
    }

    /**
     * Returns a symbol representing agent and its current status.
     * @return symbol in string
     */
    @Override
    public String toString() {
        String status;

        if (isActive()) {
            status = "+";
        } else {
            if (isJailed()) {
                status = "*";
            } else {
                status = "-";
            }
        }

        return "A" + status;
    }
}
