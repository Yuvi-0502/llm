package com.newsaggregator.server.mapper;

import com.newsaggregator.server.dto.article.ArticleDTO;
import com.newsaggregator.server.dto.article.ArticleRequest;
import com.newsaggregator.server.model.Article;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface ArticleMapper {
    @Mapping(target = "categoryName", source = "category.name")
    ArticleDTO toDTO(Article article);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "category", ignore = true)
    @Mapping(target = "savedByUsers", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    @Mapping(target = "likesCount", constant = "0")
    @Mapping(target = "dislikesCount", constant = "0")
    Article toEntity(ArticleRequest request);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "category", ignore = true)
    @Mapping(target = "savedByUsers", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    @Mapping(target = "likesCount", ignore = true)
    @Mapping(target = "dislikesCount", ignore = true)
    void updateEntityFromRequest(ArticleRequest request, @MappingTarget Article article);
} 