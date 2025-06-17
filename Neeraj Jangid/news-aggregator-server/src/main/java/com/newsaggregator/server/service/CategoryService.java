package com.newsaggregator.server.service;

import com.newsaggregator.server.model.Category;
import java.util.List;
import java.util.Optional;

public interface CategoryService {
    Category createCategory(Category category);
    Optional<Category> getCategoryById(Long id);
    Optional<Category> getCategoryByName(String name);
    List<Category> getAllCategories();
    void updateCategory(Category category);
    void deleteCategory(Long id);
    boolean existsByName(String name);
} 