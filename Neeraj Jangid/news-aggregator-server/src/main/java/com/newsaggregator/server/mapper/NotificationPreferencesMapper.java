package com.newsaggregator.server.mapper;

import com.newsaggregator.server.dto.notification.NotificationPreferencesDTO;
import com.newsaggregator.server.dto.notification.NotificationPreferencesRequest;
import com.newsaggregator.server.model.NotificationPreferences;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface NotificationPreferencesMapper {
    @Mapping(target = "categories", expression = "java(preferences.getCategories().stream().map(category -> category.getName()).collect(java.util.stream.Collectors.toSet()))")
    NotificationPreferencesDTO toDTO(NotificationPreferences preferences);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "user", ignore = true)
    @Mapping(target = "categories", ignore = true)
    NotificationPreferences toEntity(NotificationPreferencesRequest request);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "user", ignore = true)
    @Mapping(target = "categories", ignore = true)
    void updateEntityFromRequest(NotificationPreferencesRequest request, @MappingTarget NotificationPreferences preferences);
} 