package com.newsaggregator.server.service.impl;

import com.newsaggregator.server.model.NotificationPreferences;
import com.newsaggregator.server.model.User;
import com.newsaggregator.server.repository.NotificationPreferencesRepository;
import com.newsaggregator.server.service.NotificationPreferencesService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional
public class NotificationPreferencesServiceImpl implements NotificationPreferencesService {

    private final NotificationPreferencesRepository notificationPreferencesRepository;

    @Override
    public NotificationPreferences createPreferences(NotificationPreferences preferences) {
        if (notificationPreferencesRepository.findByUser(preferences.getUser()).isPresent()) {
            throw new IllegalArgumentException("Notification preferences already exist for this user");
        }
        return notificationPreferencesRepository.save(preferences);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<NotificationPreferences> getPreferencesByUser(User user) {
        return notificationPreferencesRepository.findByUser(user);
    }

    @Override
    public void updatePreferences(NotificationPreferences preferences) {
        if (!notificationPreferencesRepository.existsById(preferences.getId())) {
            throw new IllegalArgumentException("Notification preferences not found with id: " + preferences.getId());
        }
        notificationPreferencesRepository.save(preferences);
    }

    @Override
    public void deletePreferences(Long id) {
        if (!notificationPreferencesRepository.existsById(id)) {
            throw new IllegalArgumentException("Notification preferences not found with id: " + id);
        }
        notificationPreferencesRepository.deleteById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public List<NotificationPreferences> getPreferencesByCategoryIdAndEmailEnabled(Long categoryId) {
        return notificationPreferencesRepository.findByCategoryIdAndEmailEnabled(categoryId);
    }

    @Override
    @Transactional(readOnly = true)
    public List<NotificationPreferences> getPreferencesByKeywordsAndEmailEnabled(String content) {
        return notificationPreferencesRepository.findByKeywordsAndEmailEnabled(content);
    }
} 