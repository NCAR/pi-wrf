;	This script plots the wind speeds for the time period
;	Eliott Foust and Mary Haley    
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;     Load in WRF ARW file
a   =  addfile("/pi-wrf/Output/Temp_WRF_Output","r")
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;    Reading in City Data
csv_file = asciiread("/pi-wrf/WRF_System/lib/World-City-Pop.csv",-1,"string")
data     = csv_file(1:)
lats     = tofloat(str_get_field(data,2,","))
lons     = tofloat(str_get_field(data,3,","))
cities   = str_get_field(data,1,",")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;       Get Variables from WRF file
dates = wrf_user_getvar(a,"Times",-1)
ntimes = dimsizes(dates(:,0))

u_wind = wrf_user_getvar(a,"U10",-1)   ; Get all times of wind components
v_wind = wrf_user_getvar(a,"V10",-1)

wind = sqrt(u_wind^2+v_wind^2)*2.23694 ; Wind magnitude in mph
wind_max=dim_max_n(wind,0)

wind@units       = ""                  ; Labels
wind@description = ""                  ; Removing description text

wrf_lat = wrf_user_getvar(a,"XLAT",0)  ; Get lat coordinates of domain
wrf_lon = wrf_user_getvar(a,"XLONG",0) ; Get lon coordinates of domain

min_lon = min(wrf_lon)
max_lon = max(wrf_lon)
min_lat = min(wrf_lat)
max_lat = max(wrf_lat) 

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;;; 	Set Resources & Parameters
res             = True
res@gsnMaximize = True
res@gsnDraw     = False
res@gsnFrame    = False

res@mpDataBaseVersion =  "HighRes"  ; High resolution

res@mpLimitMode = "LatLon"          ; Limit the map area by lat & lon
res@mpMinLonF   =  min(wrf_lon)
res@mpMaxLonF   =  max(wrf_lon)
res@mpMinLatF   =  min(wrf_lat)
res@mpMaxLatF   =  max(wrf_lat)

res@pmTickMarkDisplayMode = "Always"
res@mpPerimOn             =  False
res@tfDoNDCOverlay        =  True
res@gsnAddCyclic          =  False


;;; Geographical Boundary Settings
res@mpOutlineBoundarySets       = "AllBoundaries"    
res@mpDataBaseVersion           = "MediumRes"
res@mpDataSetName               = "Earth..2"
res@mpGridAndLimbOn             =  False
res@mpGeophysicalLineColor      = "Black"
res@mpNationalLineColor         = "Black"
res@mpUSStateLineColor          = "Black"
res@mpCountyLineColor           = "gray50"
res@mpCountyLineThicknessF      =  1
res@mpUSStateLineThicknessF     =  6
res@mpNationalLineThicknessF    =  6
res@mpGeophysicalLineThicknessF =  6
res@mpOutlineDrawOrder          = "PostDraw"


;;; Contour Settings
res@cnLevelSelectionMode = "ManualLevels"     ; Set manual contour levels
;res@cnMinLevelValF      =  0                 ; Set min contour level
;res@cnMaxLevelValF      =  110                ; Set max contour level
res@cnLevelSpacingF      =  2                 ; Set contour spacing 
res@cnFillOn             =  True              ; Turn on contour fill
res@cnLinesOn            =  False             ; Turn off contour lines
res@cnLineLabelsOn       =  False             ; Turn off contour labels

res@cnFillOn             = True               ; Title and Labels Settings
res@lbTitleOn            = True
res@cnFillPalette        = "BlueYellowRed" 
res@lbTitleString        = "Wind Speed (mph)"
res@lbTitleFontHeightF   = .02


upper_bound = max(wind)
upper_bound = upper_bound+(10-mod(upper_bound,10))
lower_bound = 0

res@cnMinLevelValF = 0
range = upper_bound
if (range.le.10) then
    res@cnLevelSpacingF = 1
    res@cnMaxLevelValF  = upper_bound

else if(range.gt.10.and.range.le.30)
    res@cnMaxLevelValF  = 30
    res@cnLevelSpacingF = 5

else if(range.gt.30.and.range.le.60)
    res@cnLevelSpacingF = 5
    res@cnMaxLevelValF  = 60
else
    res@cnLevelSpacingF = 10
    res@cnMaxLevelValF  = upper_bound
end if
end if
end if

markerres                 =  True
markerres@gsMarkerColor   = "Black"           ; City marker settings
markerres@gsMarkerIndex   =  16
markerres@gsMarkerSizeF   =  10

;;; City marker settings
markerres                 =  True
markerres@gsMarkerColor   = "Black"
markerres@gsMarkerIndex   =  16
markerres@gsMarkerSizeF   =  10


;;;    Setting workstation
res = wrf_map_resources(a,res)
wks_type           = "png"
wks_type@wkWidth   = 2048
wks_type@wkHeight  = 2048

;;; City marker settings
markerres                 =  True
markerres@gsMarkerColor   = "Black"
markerres@gsMarkerIndex   =  16
markerres@gsMarkerSizeF   =  10

;;;    Setting workstation
res = wrf_map_resources(a,res)
wks_type           = "png"
wks_type@wkWidth   = 2048
wks_type@wkHeight  = 2048

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;     Setting up loops
do iter=0,ntimes

;;; The if statments are used to configure hourly,max,& min plots
if iter .eq. ntimes then
     res@tiXAxisString   = "Maximum Surface Winds"
     res@tiXAxisSide     = "Top"
     res@tiXAxisFont     =  "helvetica-bold"
     res@gsnStringFontHeightF = 8
     res@gsnLeftString = "Max Surface Winds Between " +\
                            chartostring(dates(0,:15))+ " and " +\
                            chartostring(dates(ntimes-1,:15))
     wks=gsn_open_wks("png","/pi-wrf/Output/max_wind")
     plot = gsn_csm_contour_map(wks,wind_max,res)

else
     res@tiXAxisString   = "Surface Windspeeds"
     res@tiXAxisSide     = "Top"
     res@tiXAxisFont     = "helvetica-bold"
     res@gsnStringFontHeightF = 8
     res@gsnLeftString   = "Forecast Hour " + sprinti("%0.2i",iter) + "~C~" +\
                           "Forecast Valid For "+\
                            chartostring(dates(iter,:15)) + " UTC"
     wks=gsn_open_wks("png","/pi-wrf/Output/hourly-wind_"+sprinti("%0.2i",iter))
     plot = gsn_csm_contour_map(wks,wind(iter,:,:),res)
end if
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;    Filtering Data
ii = ind(lats.ge.min_lat.and.lats.le.max_lat.and.lons.ge.min_lon.and.lons.le.max_lon)

;	Set Text Settings
righttext               = True
righttext@txFont        = "helvetica-bold"
righttext@txFontColor   = "Black"
righttext@txFontHeightF =  0.01
righttext@txJust        = "CenterLeft"
city_text_right=gsn_add_text(wks,plot,(cities(ii)),lons(ii),lats(ii),righttext)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
;
; Retrieve the ids of the text strings that were just added so we can
; retrieve their heights, widths, and locations. This information 
; will be used to determine if any text strings are overlaying other text
; strings.
;
nstrs=dimsizes(ii)
getvalues plot
	"pmAnnoViews" : text_ids
end getvalues

 
xndc    = new(nstrs,float)     ;  X center of box in NDC coords
yndc    = new(nstrs,float)     ;  Y center of box in NDC coords
rgt     = new(nstrs,float)     ;  Hold right position of text box.
lft     = new(nstrs,float)     ;  "    left     "     "   "    " 
top     = new(nstrs,float)     ;  "    top      "     "   "    " 
bot     = new(nstrs,float)     ;  "    bottom   "     "   "    " 
width   = new(nstrs,float)     ;  width of each text box
height  = new(nstrs,float)     ;  height of each text box
max_lat_ndc = new(1,float)     ;  Top edge of plot
max_lon_ndc = new(1,float)     ;  Right edge of plot
min_lat_ndc = new(1,float)     ;  Bottom edge of plot
min_lon_ndc = new(1,float)     ;  Left edge of plot
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;



;       Loop through and get the width and height of each box.
do i=0,nstrs-1
	getvalues text_ids(i)
		"vpWidthF"  : width(i)
		"vpHeightF" : height(i)
	end getvalues
end do
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;



;       Convert the lat/lon left-center of each box & viewport edges to NDC coordinates
;
datatondc(plot,lons(ii),lats(ii),xndc,yndc)
datatondc(plot,min_lon,min_lat,min_lon_ndc,min_lat_ndc)
datatondc(plot,max_lon,max_lat,max_lon_ndc,max_lat_ndc)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


; Calculate the four edges of each text box in NDC coordinates.
top = yndc + height/2.
bot = yndc - height/2.
lft = xndc
rgt = xndc +  width
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;



;       Now we're going to loop through each text string that has been added,
;       and compare it to all other text strings that have been added to see if
;       they overlap. If an overlap is encountered, one of the strings will be
;       tagged for removal, and a box will be drawn around it (just to show,
;       for debug purposes, which text strings are getting removed).
;
removed_list = new(nstrs,integer)
keep_list = new(nstrs,integer)
rcount = 0                         ; Number of removed text boxes.
kcount = 0                         ; Number of kept text boxes
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;



;      ibox1 is index of box that we're checking to see if it overlaps.
;      ibox2 is the index of the box that we're checking box ibox1 against.

do ibox1 = 0,nstrs-1
	ibox2 = 0
	overlap_found = False 
		do while(ibox2.lt.nstrs.and..not.overlap_found)
;
; Check if any one of the corners represented by box "ibox1" is inside
; the box representd by "ibox2".  If so, remove it.  Make sure you are
; not checking a box against itself, or against a box that has already
; been removed.
;
			if (ibox1.ne.ibox2.and.(.not.any(ibox2.eq.removed_list))) then
				if ( (top(ibox1).le.top(ibox2).and.top(ibox1).ge.bot(ibox2).and. \
					 lft(ibox1).le.rgt(ibox2).and.lft(ibox1).ge.lft(ibox2)).or. \
                                	(bot(ibox1).le.top(ibox2).and.bot(ibox1).ge.bot(ibox2).and. \
                                 	lft(ibox1).le.rgt(ibox2).and.lft(ibox1).ge.lft(ibox2)).or. \
                                	(bot(ibox1).le.top(ibox2).and.bot(ibox1).ge.bot(ibox2).and. \
                                	 rgt(ibox1).le.rgt(ibox2).and.rgt(ibox1).ge.lft(ibox2)).or. \
                                	(top(ibox1).le.top(ibox2).and.top(ibox1).ge.bot(ibox2).and. \
                                 	rgt(ibox1).le.rgt(ibox2).and.rgt(ibox1).ge.lft(ibox2)).or. \
					rgt(ibox1).ge.max_lon_ndc.or.lft(ibox1).le.min_lon_ndc.or.\
					top(ibox1).ge.max_lat_ndc.or.bot(ibox1).le.min_lat_ndc) then
        
                                 	overlap_found = True            ; Mark that an overlap has been found.

                                 	removed_list(rcount) = ibox1    ; Update removed_list and
                                 	rcount = rcount + 1             ; its counter.
				end if
			end if
		ibox2 = ibox2 + 1                                        ; Update the box counter
		end do	
    if(.not.overlap_found) then
    	keep_list(kcount) = ibox1
    	kcount = kcount +1
    end if
end do
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Here's the code that removes the overlapping text strings.
 NhlRemoveAnnotation(plot,text_ids(removed_list(:rcount-1)))
 delete(text_ids)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
lon_marker=lons(ii)
lat_marker=lats(ii)
city_markers=gsn_add_polymarker(wks,plot,lon_marker(keep_list(:kcount-1)),lat_marker(keep_list(:kcount-1)),markerres)

draw(plot)
frame(wks)
end do
