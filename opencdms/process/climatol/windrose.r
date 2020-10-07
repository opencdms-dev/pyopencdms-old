#- windrose.- Wind rose from a data frame with columns: DateTime, Dir, Speed.
# Version 1.0 (2020-08-08), by Jose A. Guijarro. (GPL license >= 2.0).
#---------------------------------------------------------------------------
# data: Data frame with columns 'DateTime, Dir, Speed'
# code: Station code
# name: Station name
# uni='m/s': Wind speed units (for the legend).
# maxnsc=8 : Maximum number of wind speed classes.
# fnum=4 : Number of reference circles to plot.
# fint=5 : Frequency intervals (in %) of the reference circles.
# flab=2 : Which circles must be labelled. 1=outer circle only; 2=all.
# col=rainbow(10,.5,.92,start=.33,end=.2) : Colors to fill the polygons.
# ang=3*pi/16 : Angle along which circles will be labelled.
# margin=c(0, 0, 4, 0) : Margins vector for the plot.
#---------------------------------------------------------------
windrose <- function(data, code='', name='', uni='m/s', maxnsc=8, fnum=4,
  fint=5, flab=2, col=rainbow(10,.5,.92,start=.33,end=.2), ang=3*pi/16,
  margin=c(0,0,4,0)) {

  #----------- compute frequencies by directions ---------------
  z <- range(data[,1]) #round date/time to just date:
  startdate <- as.Date(z[1]); enddate <- as.Date(z[2])
  dd <- data[,2]; vv <- data[,3]; rm(data)
  dd[dd<0 | dd>360] <- NA #avoid bad or variable direction values
  vv[is.na(dd)] <- NA #avoid speeds with missing direction
  nd <- sum(!is.na(vv)) #nr. of available data
  if(nd==0) stop('No data available for that station and dates\n')
  cal <- sum(vv==0,na.rm=TRUE) #nr. of calm wind observations
  dd <- round(dd/360*16+1); dd[dd==17] <- 1 #direction classes
  vm <- tapply(vv,as.factor(dd),mean,na.rm=TRUE) #mean speed by direction
  vx <- tapply(vv,as.factor(dd),max,na.rm=TRUE) #max. speed by direction
  vmt <- mean(vv,na.rm=TRUE) #overall mean speed
  vmx <- max(vv,na.rm=TRUE) #overall max. speed
  vv[vv==0] <- NA #remove calm observations
  dd[is.na(vv)] <- NA #avoid directions with missing speed
  vvc <- pretty(vv) #speed classes
  nvvc <- length(vvc)-1 #number of speed classes
  #convert wind speeds to factor classes:
  if(nvvc>maxnsc) { #if too many speed classes, limit their number:
    nvvc <- maxnsc
    vvf <- cut(vv,c(vvc[1:maxnsc],999))
    spclasses <- paste(vvc[1:nvvc],vvc[2:(nvvc+1)],sep='-')
    if(latex) spclasses[nvvc] <- paste('>=',vvc[maxnsc])
    else spclasses[nvvc] <- paste('>=',vvc[maxnsc])
    geflag <- TRUE
  } else {
    vvf <- cut(vv,vvc)
    spclasses <- paste(vvc[1:nvvc],vvc[2:(nvvc+1)],sep='-')
    geflag <- FALSE
  }
  #compute the frequency table:
  fr <- table(vvf,dd)
  #if there are void direction classes, fill them with zeroes:
  z <- as.integer(colnames(fr))
  if(length(z)<16) {
    zrn <- rownames(fr)
    zm <- matrix(rep(0,16*nrow(fr)),dim(fr))
    zm[,z] <- fr
    fr <- zm
    colnames(fr) <- as.character(1:16) 
    rownames(fr) <- zrn
  }
  #distribute calms in the first speed class:
  nd1 <- sum(fr[1,]); fr[1,] <- fr[1,] * (nd1+cal)/nd1
  if(nd>0) fr <- fr*100./nd #compute frequencies as percentages
  frt <- apply(fr,1,sum) #sum frequencies by speed classes
  frtd <- apply(fr,2,sum) #sum frequencies by direction classes
  #----------- build the table of frequencies ------------------
  tab <- cbind(fr,frt)
  tab <- round(rbind(tab,c(frtd,sum(frtd))),1)
  tab <- data.frame(rbind(tab,round(c(vm,vmt),1),round(c(vx,vmx),1)))
  names(tab) <- c('N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW',
    'WSW','W','WNW','NW','NNW','Total')
  row.names(tab) <- c(spclasses,'Total','Mean Sp.','Mx.M.Sp.')
  #----------- plot the windrose -------------------------------
  old.par <- par(no.readonly = TRUE)
  on.exit(par(old.par))
  fr <- tab[1:nvvc,1:16]
  if(geflag) row.names(fr)[nvvc] <- paste('>=',vvc[nvvc])
  ndir <- 16 #nr. of direction classes
  nr <- nvvc #nr. of speed classes
  fmax <- fnum*fint #max. frequency to be circled
  key <- (nr>1) #legend if more than one speed class
  #make room for the legend at the left side:
  if(key) mlf <- 3 else mlf <- 1  #left margin factor
  par(mar=margin, new=FALSE)    #windrose margin
  # x,y components for every wind direction and plot settings:
  fx <- cos(pi/2-(2*pi/ndir*0:(ndir-1)))
  fy <- sin(pi/2-(2*pi/ndir*0:(ndir-1)))
  plot(fx,fy,xlim=c(-fmax-mlf*fint,fmax+fint),ylim=c(-fmax-fint,fmax+fint),
    xaxt="n",yaxt="n",xlab="",ylab="",bty="n",asp=1,type="n")
  if(nr==1) {  #only one speed class
    cx <- fx*fr
    cy <- fy*fr
  }
  else {  #more than one speed classes
    f <- apply(fr,2,sum)
    cx <- fx*f
    cy <- fy*f
    for(i in nr:2) {
      f <- f-fr[i,]
      cx <- c(cx,NA,fx*f)
      cy <- c(cy,NA,fy*f)
    }
  }
  polygon(cx,cy,col=col[nr:1])
  symbols(c(0*1:fnum),c(0*1:fnum),circles=c(fint*1:fnum),inches=FALSE,add=TRUE)
  segments(0*1:ndir,0*1:ndir,fmax*fx,fmax*fy)
  fmaxi <- fmax+fint/4
  text(0,fmaxi,"N")
  text(0,-fmaxi,"S")
  text(fmaxi,0,"E")
  text(-fmaxi,0,"W")
  if(flab==2)
    for(i in 1:fnum) text(i*fint*cos(ang),i*fint*sin(ang),paste(i*fint,"%"))
  else if(flab==1)
    text(fmax*cos(ang),fmax*sin(ang),paste(fmax,"%"))
  if(key) { #legend
    legend(-fmaxi-2.3*fint,fmaxi+2,fill=col,legend=spclasses)
    text(-fmaxi-1.5*fint,fmaxi+.9*fint,uni)
  }
  title(paste(name,'windrose\n',startdate,'to',enddate))
  invisible(tab)
}
