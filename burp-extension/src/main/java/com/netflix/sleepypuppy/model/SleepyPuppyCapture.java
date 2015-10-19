package com.netflix.sleepypuppy.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import javax.xml.bind.annotation.XmlRootElement;

/**
 * Created by rperam on 10/2/15.
 */
@XmlRootElement
public class SleepyPuppyCapture {

    private String cookies;
    private String screenshot;
    private String dom;
    private String url;
    private String referrer;
    private String pub_date;
    private int payload;
    private int id;
    private String user_agent;
    private String assessment;

    public SleepyPuppyCapture() {
    }

    public SleepyPuppyCapture(String cookies, String screenshot, String dom, String url, String referrer, String pub_date, int payload, int id, String user_agent, String assessment) {
        this.cookies = cookies;
        this.screenshot = screenshot;
        this.dom = dom;
        this.url = url;
        this.referrer = referrer;
        this.pub_date = pub_date;
        this.payload = payload;
        this.id = id;
        this.user_agent = user_agent;
        this.assessment = assessment;
    }

    @JsonProperty("cookies")
    public String getCookies() {
        return cookies;
    }

    public void setCookies(String cookies) {
        this.cookies = cookies;
    }

    @JsonProperty("screenshot")
    public String getScreenshot() {
        return screenshot;
    }

    public void setScreenshot(String screenshot) {
        this.screenshot = screenshot;
    }

    @JsonProperty("dom")
    public String getDom() {
        return dom;
    }

    public void setDom(String dom) {
        this.dom = dom;
    }

    @JsonProperty("url")
    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    @JsonProperty("referrer")
    public String getReferrer() {
        return referrer;
    }

    public void setReferrer(String referrer) {
        this.referrer = referrer;
    }

    @JsonProperty("pub_date")
    public String getPub_date() {
        return pub_date;
    }

    public void setPub_date(String pub_date) {
        this.pub_date = pub_date;
    }

    @JsonProperty("payload")
    public int getPayload() {
        return payload;
    }

    public void setPayload(int payload) {
        this.payload = payload;
    }

    @JsonProperty("id")
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
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
}

