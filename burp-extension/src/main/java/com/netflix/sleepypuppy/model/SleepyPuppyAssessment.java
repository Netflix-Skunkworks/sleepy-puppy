package com.netflix.sleepypuppy.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import javax.xml.bind.annotation.XmlRootElement;

/**
 * Created by rperam on 9/14/15.
 */
@XmlRootElement
public class SleepyPuppyAssessment {
    private boolean snooze;
    private boolean run_once;
    private String id;
    private boolean access_log_enabled;
    private String name;

    public SleepyPuppyAssessment() {
    }

    public SleepyPuppyAssessment(boolean snooze, boolean run_once, String id,
                                 boolean access_log_enabled, String name) {
        this.snooze = snooze;
        this.run_once = run_once;
        this.id = id;
        this.access_log_enabled = access_log_enabled;
        this.name = name;
    }

    @JsonProperty("snooze")
    public boolean isSnooze() {
        return snooze;
    }

    public void setSnooze(boolean snooze) {
        this.snooze = snooze;
    }

    @JsonProperty("run_once")
    public boolean isRun_once() {
        return run_once;
    }

    public void setRun_once(boolean run_once) {
        this.run_once = run_once;
    }

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    @JsonProperty("access_log_enabled")
    public boolean isAccess_log_enabled() {
        return access_log_enabled;
    }

    public void setAccess_log_enabled(boolean access_log_enabled) {
        this.access_log_enabled = access_log_enabled;
    }

    @JsonProperty("name")
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
