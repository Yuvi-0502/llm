package com.newsaggregator.server.mapper;

import com.newsaggregator.server.dto.category.CategoryDTO;
import com.newsaggregator.server.dto.category.CategoryRequest;
import com.newsaggregator.server.model.Category;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface CategoryMapper {
    CategoryDTO toDTO(Category category);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "articles", ignore = true)
    @Mapping(target = "notificationPreferences", ignore = true)
    Category toEntity(CategoryRequest request);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "articles", ignore = true)
    @Mapping(target = "notificationPreferences", ignore = true)
    void updateEntityFromRequest(CategoryRequest request, @MappingTarget Category category);
} 