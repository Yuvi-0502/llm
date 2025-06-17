package com.newsaggregator.server.dto.notification;

import lombok.Data;
import java.util.Set;

@Data
public class NotificationPreferencesRequest {
    private Set<String> categories;
    private Set<String> keywords;
    private boolean emailNotificationsEnabled;
    private boolean pushNotificationsEnabled;
} 