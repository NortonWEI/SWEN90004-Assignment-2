import java.util.Random;

public class Agent extends Thread {
    private boolean isActive = false;
    private int jailTerm = 0;
    private double riskAversion;
    private double perceivedHardship;
    private double grievance;
    private double estimatedArrestProbability;
    private double netRisk;

    public Agent() {
        Random rnd = new Random(1);
        perceivedHardship = rnd.nextDouble();
        riskAversion = rnd.nextDouble();
        grievance = perceivedHardship * (1 - Params.GOVERNMENT_LEGITIMACY);


    }

    public void run() {
        while (!isInterrupted()) {

        }
    }

    private void move() {

    }

    public boolean isActive() {
        return isActive;
    }

    public void setActive(boolean active) {
        isActive = active;
    }

    public int getJailTerm() {
        return jailTerm;
    }

    public void setJailTerm(int jailTerm) {
        this.jailTerm = jailTerm;
    }

    public double getRiskAversion() {
        return riskAversion;
    }

    public void setRiskAversion(float riskAversion) {
        this.riskAversion = riskAversion;
    }

    public double getPerceivedHardship() {
        return perceivedHardship;
    }

    public void setPerceivedHardship(float perceivedHardship) {
        this.perceivedHardship = perceivedHardship;
    }
}
