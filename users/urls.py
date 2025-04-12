from django.urls import path
from .views.createUser import createUser
from .views.signIn import signIn
from .views.usersGenreSelection import genreSelection
from .views.usersLAnguageSelection import usersLanguaseSelection
from .views.usersContentLanguageList import usersContentLanguageList
from .views.userGenreList import genreList
from .views.userTrendingMovies import UserTrendingVideos
from .views.shortTrendingSection import TrailerTrendingSection
from .views.getProfileDetails import getProfileDetails
from .views.editProfileDetails import editProfileDetails
from .views.serachItem import serachItem
from .views.dailyCheckinTask import dailyCheckInTask
from .views.collectCheciNPoints import collectCheckInPoint
from .views.markAsBookMark import markAsBookMark
from .views.getBookMark import getBookMark
from .views.likeVideo import likeVideo
from .views.getAds import getAds
from .views.checkSignedVideo import checkSignedVideo
from .views.googleAuth import googleAuth
from .views.getPackage import getPackage
from .views.fetchWalletPoints import fetchWalletPoints
from .views.forgotPassword import forgotPassword
from .views.verifyOtp import verifyOtp
from .views.updatePassword import updatePassword
from .views.getUserMintsPurchaseHistory import getUserMintPurchaseHistory
from .views.continueWatchingHistory import continueWatchingHistorySaving
from .views.getContinueWatchingHistory import getUserWatchHistory

urlpatterns = [
    path("register/", createUser),
    path("signIn/", signIn),
    path("genreList/", genreList),
    path("genreSelector/", genreSelection),
    path("languageList/", usersContentLanguageList),
    path("languageSelector/", usersLanguaseSelection),
    path("trendingMovies/", UserTrendingVideos),
    path("trendingTrailers/", TrailerTrendingSection),
    path("getUserDetails/", getProfileDetails),
    path("editUserDetails/", editProfileDetails),
    path("searchItem/", serachItem),
    path("checkInTask/", dailyCheckInTask),
    path("collectCheckIn/", collectCheckInPoint),
    path("markBookMark/", markAsBookMark),
    path("getBookMark/", getBookMark),
    path("likeVideo/", likeVideo),
    path("getAds/<path>/<sessionType>", getAds),
    path("checkSignedVideo/", checkSignedVideo),
    path("getPackage/", getPackage),
    path("googleAuth/", googleAuth),
    path("fetchWallet/", fetchWalletPoints),
    path("forgotPassword/", forgotPassword),
    path("verifyOtp/", verifyOtp),
    path("updatePassword/", updatePassword),
    path("mintsPurchaseHistory/", getUserMintPurchaseHistory),
    path("continueWatching/", continueWatchingHistorySaving),
    path("getContinueWatching/", getUserWatchHistory),
]
