package com.newsaggregator.server.controller;

import com.newsaggregator.server.dto.notification.NotificationPreferencesDTO;
import com.newsaggregator.server.dto.notification.NotificationPreferencesRequest;
import com.newsaggregator.server.mapper.NotificationPreferencesMapper;
import com.newsaggregator.server.model.NotificationPreferences;
import com.newsaggregator.server.model.User;
import com.newsaggregator.server.service.NotificationPreferencesService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/notifications/preferences")
@RequiredArgsConstructor
public class NotificationPreferencesController {

    private final NotificationPreferencesService notificationPreferencesService;
    private final NotificationPreferencesMapper notificationPreferencesMapper;

    @GetMapping
    public ResponseEntity<NotificationPreferencesDTO> getPreferences(
            @AuthenticationPrincipal User user) {
        NotificationPreferences preferences = notificationPreferencesService.getPreferences(user);
        return ResponseEntity.ok(notificationPreferencesMapper.toDTO(preferences));
    }

    @PutMapping
    public ResponseEntity<NotificationPreferencesDTO> updatePreferences(
            @AuthenticationPrincipal User user,
            @Valid @RequestBody NotificationPreferencesRequest request) {
        NotificationPreferences preferences = notificationPreferencesService.getPreferences(user);
        notificationPreferencesMapper.updateEntityFromRequest(request, preferences);
        NotificationPreferences updatedPreferences = notificationPreferencesService.updatePreferences(preferences);
        return ResponseEntity.ok(notificationPreferencesMapper.toDTO(updatedPreferences));
    }

    @PostMapping("/categories/{categoryName}")
    public ResponseEntity<NotificationPreferencesDTO> addCategory(
            @AuthenticationPrincipal User user,
            @PathVariable String categoryName) {
        NotificationPreferences preferences = notificationPreferencesService.addCategory(user, categoryName);
        return ResponseEntity.ok(notificationPreferencesMapper.toDTO(preferences));
    }

    @DeleteMapping("/categories/{categoryName}")
    public ResponseEntity<NotificationPreferencesDTO> removeCategory(
            @AuthenticationPrincipal User user,
            @PathVariable String categoryName) {
        NotificationPreferences preferences = notificationPreferencesService.removeCategory(user, categoryName);
        return ResponseEntity.ok(notificationPreferencesMapper.toDTO(preferences));
    }
} 