import java.util.Random;

public class Cop extends Thread {

    public Cop() {

    }

    public void run() {
        while (!isInterrupted()) {

        }
    }

    private void move() {

    }

    private Agent jailAgent(Agent agent) {
        Random rnd = new Random(Params.MAX_JAILED_TERM + 1);
        agent.setJailTerm(rnd.nextInt());

        return agent;
    }
}
