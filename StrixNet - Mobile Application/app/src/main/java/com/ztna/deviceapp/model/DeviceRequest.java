package com.ztna.deviceapp.model;

public class DeviceRequest {
    private final String deviceName;
    private final String ipAddress;
    private final String macAddress; // a.k.a. device_id
    private final String uuid;

    public DeviceRequest(String deviceName, String ipAddress, String macAddress, String uuid) {
        this.deviceName = deviceName;
        this.ipAddress = ipAddress;
        this.macAddress = macAddress;
        this.uuid = uuid;
    }

    public String getDeviceName() {
        return deviceName;
    }

    public String getIpAddress() {
        return ipAddress;
    }

    public String getMacAddress() {
        return macAddress;
    }

    public String getUuid() {
        return uuid;
    }
}
