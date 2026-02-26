"""
GraphQL query definitions for Mytheresa API
"""


# Product listing query with all necessary fields
PRODUCT_LISTING_QUERY = """query XProductListingPageQuery($filtersQueryParams: String, $page: Int, $size: Int, $slug: String, $sort: String) {
  xProductListingPage: xProductListingPageV2(filtersQueryParams: $filtersQueryParams, page: $page, size: $size, slug: $slug, sort: $sort) {
    id
    pagination {
      currentPage
      itemsPerPage
      totalItems
      totalPages
    }
    products {
      color
      department
      description
      designer
      designerErpId
      displayImages
      hasStock
      mainPrice
      name
      price {
        currencyCode
        currencySymbol
        discount
        original
        percentage
      }
      sku
      slug
    }
  }
}"""


def build_listing_variables(
    slug: str,
    page: int = 1,
    size: int = 60,
    sort: str = None,
    filters: str = ""
  ) -> dict:
    """
    Build variables for product listing query
    
    Args:
        slug: Category slug (e.g., "/clothing", "/designers/gucci")
        page: Page number (1-indexed)
        size: Items per page
        sort: Sort parameter
        filters: Filter query params
        
    Returns:
        Variables dictionary
    """
    return {
        "page": page,
        "size": size,
        "slug": slug,
        "sort": sort,
        "filtersQueryParams": filters
    }
