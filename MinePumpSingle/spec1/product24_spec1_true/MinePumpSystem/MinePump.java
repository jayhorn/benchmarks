package MinePumpSystem; 

import MinePumpSystem.Environment; 

public   class  MinePump {
	

	boolean pumpRunning = false;

	

	boolean systemActive = true;

	

	Environment env;

	

	public MinePump(Environment env) {
		super();
		this.env = env;
	}

	

	public void timeShift() {
		if (pumpRunning)
			env.lowerWaterLevel();
		if (systemActive)
			processEnvironment();
	}

	
	private void  processEnvironment__wrappee__base  () {
		
	}

	

	private void  processEnvironment__wrappee__lowWaterSensor  () {
		if (pumpRunning && isLowWaterLevel()) {
			deactivatePump();
		} else {
			processEnvironment__wrappee__base();
		}
	}

	
	public void processEnvironment() {
		if (pumpRunning && isMethaneAlarm()) {
			deactivatePump();
		} else {
			processEnvironment__wrappee__lowWaterSensor();
		}
	}

	

	void activatePump() {
		pumpRunning = true;
	}

	

	public boolean isPumpRunning() {
		return pumpRunning;
	}


	void deactivatePump() {
		pumpRunning = false;
	}

	
	
	boolean isMethaneAlarm() {
		return env.isMethaneLevelCritical();
	}

	

	@Override
	public String toString() {
		return "Pump(System:" + (systemActive?"On":"Off") + ",Pump:" + (pumpRunning?"On":"Off") +") " + env.toString(); 
	}

	
	
	public Environment getEnv() {
		return env;
	}

	
	
	boolean isLowWaterLevel() {
		return !env.isLowWaterSensorDry();
	}

	
	public void stopSystem() {
		if (pumpRunning) {
			deactivatePump();
		}
		assert !pumpRunning;
		systemActive = false;
	}

	
	public void startSystem() {
		assert !pumpRunning;
		systemActive = true;
	}


	public boolean isSystemActive() {
		return systemActive;
	}


}
