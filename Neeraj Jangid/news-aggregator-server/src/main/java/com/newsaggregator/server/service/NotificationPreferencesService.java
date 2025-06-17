package com.newsaggregator.server.service;

import com.newsaggregator.server.model.NotificationPreferences;
import com.newsaggregator.server.model.User;
import java.util.List;
import java.util.Optional;

public interface NotificationPreferencesService {
    NotificationPreferences createPreferences(NotificationPreferences preferences);
    Optional<NotificationPreferences> getPreferencesByUser(User user);
    void updatePreferences(NotificationPreferences preferences);
    void deletePreferences(Long id);
    List<NotificationPreferences> getPreferencesByCategoryIdAndEmailEnabled(Long categoryId);
    List<NotificationPreferences> getPreferencesByKeywordsAndEmailEnabled(String content);
} 