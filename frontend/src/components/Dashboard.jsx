import { ArrowRight, Database, Search, Shield, Target, TrendingUp, Sparkles, Award } from 'lucide-react'
import Card from './UI/Card'
import Button from './UI/Button'

function Dashboard({ onNavigate }) {
  const features = [
    {
      icon: Target,
      title: 'Akurasi Tinggi',
      description: 'Teknologi SVM + AdaBoost dengan akurasi 93.7% melalui validasi silang K=10',
      color: 'from-blue-500 to-blue-600'
    },
    {
      icon: Database,
      title: 'Dataset Lengkap',
      description: 'Database produk makanan dengan 8+ kategori alergen utama',
      color: 'from-green-500 to-green-600'
    },
    {
      icon: Shield,
      title: 'Keamanan Pangan',
      description: 'Deteksi dini alergen untuk melindungi konsumen sensitif',
      color: 'from-purple-500 to-purple-600'
    }
  ]

  const stats = [
    { label: 'Jenis Alergen', value: '8+', icon: Target },
    { label: 'Dataset Training', value: '399', icon: Database },
    { label: 'Akurasi Model', value: '93.7%', icon: Award },
    { label: 'Processing Time', value: '<500ms', icon: TrendingUp }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          
          {/* Badge */}
          <div className="flex justify-center mb-8">
            <div className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-100 to-blue-200 text-blue-800 rounded-full text-sm font-semibold border border-blue-300">
              <Sparkles className="h-4 w-4 mr-2" />
              Sistem AI - Universitas Nasional Karangturi
            </div>
          </div>
          
          {/* Main Title */}
          <div className="text-center mb-12">
            <h1 className="text-5xl md:text-7xl font-bold text-slate-900 mb-6 leading-tight">
              SUPERBOOST
              <span className="block bg-gradient-to-r from-blue-600 via-purple-600 to-blue-700 bg-clip-text text-transparent">
                ALLERSCAN
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-slate-600 max-w-4xl mx-auto leading-relaxed mb-8">
              Sistem Deteksi Alergen pada Produk Pangan Berbasis 
              <span className="font-semibold text-blue-600"> Machine Learning SVM + AdaBoost</span>
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6">
              <Button 
                size="lg"
                onClick={() => onNavigate('form')}
                className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-8 py-4 text-lg font-semibold rounded-2xl shadow-xl hover:shadow-blue-500/25 transform hover:scale-105 transition-all duration-300"
              >
                <Search className="h-6 w-6 mr-3" />
                Mulai Analisis Alergen
              </Button>
              <Button 
                variant="secondary"
                onClick={() => onNavigate('dataset')}
                className="bg-white hover:bg-slate-50 border-2 border-slate-200 hover:border-slate-300 text-slate-700 px-8 py-4 text-lg font-semibold rounded-2xl shadow-lg"
              >
                <Database className="h-6 w-6 mr-3" />
                Lihat Dataset
              </Button>
            </div>
          </div>
        </div>
        
        {/* Background Decoration */}
        <div className="absolute top-0 left-0 right-0 bottom-0 opacity-5 pointer-events-none">
          <div className="absolute top-20 left-20 w-72 h-72 bg-blue-500 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-500 rounded-full blur-3xl"></div>
        </div>
      </div>

      {/* Statistics Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-slate-900 mb-4">Performance & Capabilities</h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Teknologi terdepan dengan hasil yang dapat diandalkan
          </p>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
          {stats.map((stat, index) => {
            const Icon = stat.icon
            return (
              <Card key={index} className="p-6 text-center bg-white rounded-3xl shadow-lg border border-slate-200 hover:shadow-xl transition-shadow duration-300">
                <div className="p-3 bg-gradient-to-r from-blue-100 to-blue-200 rounded-2xl w-fit mx-auto mb-4">
                  <Icon className="h-8 w-8 text-blue-600" />
                </div>
                <div className="text-3xl font-bold text-slate-900 mb-2">{stat.value}</div>
                <div className="text-slate-600 font-medium">{stat.label}</div>
              </Card>
            )
          })}
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-slate-900 mb-4">Keunggulan Sistem</h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Fitur-fitur canggih untuk deteksi alergen yang akurat dan efisien
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <Card key={index} className="p-8 bg-white rounded-3xl shadow-lg border border-slate-200 hover:shadow-xl transition-all duration-300 group">
                <div className={`p-4 bg-gradient-to-r ${feature.color} rounded-2xl w-fit mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <Icon className="h-10 w-10 text-white" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-4">{feature.title}</h3>
                <p className="text-slate-600 leading-relaxed">{feature.description}</p>
              </Card>
            )
          })}
        </div>
      </div>

      {/* How It Works Section */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">Cara Kerja Sistem</h2>
            <p className="text-lg text-slate-300 max-w-2xl mx-auto">
              Proses analisis alergen dalam 3 langkah sederhana
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '01',
                title: 'Input Data Produk',
                description: 'Masukkan informasi produk makanan dan bahan-bahan yang digunakan'
              },
              {
                step: '02', 
                title: 'Analisis AI',
                description: 'Sistem menganalisis menggunakan algoritma SVM + AdaBoost yang telah dilatih'
              },
              {
                step: '03',
                title: 'Hasil & Rekomendasi',
                description: 'Dapatkan hasil deteksi alergen dengan tingkat confidence yang akurat'
              }
            ].map((item, index) => (
              <div key={index} className="text-center">
                <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center text-2xl font-bold text-white mx-auto mb-6">
                  {item.step}
                </div>
                <h3 className="text-xl font-bold text-white mb-4">{item.title}</h3>
                <p className="text-slate-300 leading-relaxed">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <Card className="p-12 bg-gradient-to-r from-blue-50 to-blue-100 border-blue-200 rounded-3xl text-center">
          <div className="p-4 bg-blue-600 rounded-2xl w-fit mx-auto mb-6">
            <Shield className="h-12 w-12 text-white" />
          </div>
          <h2 className="text-3xl font-bold text-slate-900 mb-4">
            Siap Menganalisis Produk Makanan Anda?
          </h2>
          <p className="text-lg text-slate-600 mb-8 max-w-2xl mx-auto">
            Mulai deteksi alergen sekarang untuk memastikan keamanan konsumen dengan teknologi AI terdepan
          </p>
          <Button 
            size="lg"
            onClick={() => onNavigate('form')}
            className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-8 py-4 text-lg font-semibold rounded-2xl shadow-xl transform hover:scale-105 transition-all duration-300"
          >
            <Target className="h-6 w-6 mr-3" />
            Mulai Analisis Sekarang
            <ArrowRight className="h-6 w-6 ml-3" />
          </Button>
        </Card>
      </div>

    </div>
  )
}

export default Dashboard
