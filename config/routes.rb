Rails.application.routes.draw do
  get 'welcome/index'
  root 'welcome#index'

  get 'new_crawl' => 'crawl#new', :as => "new_crawl"

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
