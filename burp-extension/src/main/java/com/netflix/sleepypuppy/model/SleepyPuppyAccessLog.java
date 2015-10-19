package com.netflix.sleepypuppy.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import javax.xml.bind.annotation.XmlRootElement;

/**
 * Created by rperam on 10/2/15.
 */
@XmlRootElement
public class SleepyPuppyAccessLog {
    private int id;
    private int payload;
    private String referrer;
    private String ip_address;
    private String user_agent;
    private String assessment;
    private String pub_date;

    public SleepyPuppyAccessLog() {
    }

    public SleepyPuppyAccessLog(int id, int payload, String referrer, String ip_address, String user_agent, String assessment, String pub_date) {
        this.id = id;
        this.payload = payload;
        this.referrer = referrer;
        this.ip_address = ip_address;
        this.user_agent = user_agent;
        this.assessment = assessment;
        this.pub_date = pub_date;
    }

    @JsonProperty("id")
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    @JsonProperty("payload")
    public int getPayload() {
        return payload;
    }

    public void setPayload(int payload) {
        this.payload = payload;
    }

    @JsonProperty("referrer")
    public String getReferrer() {
        return referrer;
    }

    public void setReferrer(String referrer) {
        this.referrer = referrer;
    }

    @JsonProperty("ip_address")
    public String getIp_address() {
        return ip_address;
    }

    public void setIp_address(String ip_address) {
        this.ip_address = ip_address;
    }

    @JsonProperty("user_agent")
    public String getUser_agent() {
        return user_agent;
    }

    public void setUser_agent(String user_agent) {
        this.user_agent = user_agent;
    }

    @JsonProperty("assessment")
    public String getAssessment() {
        return assessment;
    }

    public void setAssessment(String assessment) {
        this.assessment = assessment;
    }

    @JsonProperty("pub_date")
    public String getPub_date() {
        return pub_date;
    }

    public void setPub_date(String pub_date) {
        this.pub_date = pub_date;
    }
}
