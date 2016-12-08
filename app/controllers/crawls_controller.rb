class CrawlsController < ApplicationController
	

	def index
		@crawls = Crawl.all
	end

	def show
		@crawl = Crawl.find(params[:id])
	end

	def new
		@crawl = Crawl.new
		puts %x( python ~/projects/Spider/lib/fuzzer/src/spider.py discover http://localhost:3001 )
	end

	def edit
		@crawl = Crawl.find(params[:id])
	end
	
	def create
		@crawl = Crawl.new( crawl_params )
		
		if @crawl.save
			redirect_to @crawl
		else
			render 'new'
		end
	end

	def update
		@crawl = Crawl.find(params[:id])

		if @crawl.update(crawl_params)
			redirect_to @crawl
		else
			render 'edit'
		end
	end

	def destroy
		@crawl = Crawl.find(params[:id])
		@crawl.destroy

		redirect_to crawls_path
	end

	private
		def crawl_params
			params.require(:crawl).permit(:app_url)
		end
end
